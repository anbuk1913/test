[http://localhost:4320/auth/practice/verification/af0e4753-2dab-4551-90a4-1aea4fd06e72](http://localhost:4320/auth/location/verification/4e13a7f6-10dd-4661-ac6c-0766e9ce0203)

http://localhost:4320/auth/location/verification/4e13a7f6-10dd-4661-ac6c-0766e9ce0203
    
    python -m venv venv
    .\venv\Scripts\activate
    python train_cpu.py
    python test_model.py

.

    pip install transformers datasets accelerate sentencepiece huggingface_hub
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    python -m pip install --upgrade pip
.


.

    https://huggingface.co/google/gemma-3-1b-it


App.py

    # app.py
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import Optional
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    from starlette.concurrency import run_in_threadpool
    
    app = FastAPI(title="Fine-tuned Gemma3 API")
    
    MODEL_PATH = "./fine_gemma3"
    
    # Pydantic model for request body
    class GenerateRequest(BaseModel):
        prompt: str
        max_new_tokens: Optional[int] = 80
        temperature: Optional[float] = 0.7
        top_p: Optional[float] = 0.9
        do_sample: Optional[bool] = True
        return_full_text: Optional[bool] = False  # if True, return prompt+generation
    
    # Pydantic model for response
    class GenerateResponse(BaseModel):
        generated_text: str
    
    # Load tokenizer & model ONCE on startup
    @app.on_event("startup")
    def load_model():
        global tokenizer, model, device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        # Ensure pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        model.to(device)
        model.eval()
    
    # Internal blocking generation function (runs in threadpool)
    def _generate_sync(
        prompt: str,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
        do_sample: bool,
        return_full_text: bool,
    ):
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        if return_full_text:
            return decoded
        # strip prompt prefix if present
        if decoded.startswith(prompt):
            return decoded[len(prompt) :].lstrip()
        return decoded
    
    # Async endpoint that delegates generation to threadpool
    @app.post("/generate", response_model=GenerateResponse)
    async def generate(req: GenerateRequest):
        if not req.prompt or req.prompt.strip() == "":
            raise HTTPException(status_code=400, detail="Prompt must not be empty.")
        try:
            generated = await run_in_threadpool(
                _generate_sync,
                req.prompt,
                req.max_new_tokens,
                req.temperature,
                req.top_p,
                req.do_sample,
                req.return_full_text,
            )
            return {"generated_text": generated}
        except RuntimeError as e:
            # common runtime errors (OOM, etc.)
            raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")



requirements.txt

    fastapi
    uvicorn[standard]
    transformers
    torch
    sentencepiece      # if tokenizer needs it (install only if required)


Run the server (development)

    python -m venv venv
    source venv/bin/activate      # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt

.
POST METHOD

    http://localhost:8000/generate 
    


Example Code in node.js

    // node-fetch or modern node
    const fetch = require('node-fetch');
    
    async function call() {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
          prompt: "Q: What are symptoms of anemia?\nA:",
          max_new_tokens: 80
        })
      });
      const json = await res.json();
      console.log(json.generated_text);
    }
    call();
