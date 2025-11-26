from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "./fine_gemma3"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

prompt = (
    "Instruction: If you are a doctor, please answer the medical questions below with general wellness guidance only.\n"
    "Question: What are the symptoms of anemia?\n"
    "Answer:"
)

inputs = tokenizer(prompt, return_tensors="pt")

output = model.generate(
    **inputs,
    max_new_tokens=80,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

print(tokenizer.decode(output[0], skip_special_tokens=True))





# ----------------------------------------------------------------------------------------------------




# from transformers import AutoTokenizer, AutoModelForCausalLM

# model_path = "./fine_gpt2"

# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# prompt = (
#     "Instruction: If you are a doctor, please answer the medical questions below with general wellness guidance only.\n"
#     "Question: What are the symptoms of anemia?\n"
#     "Answer:"
# )

# inputs = tokenizer(prompt, return_tensors="pt")

# output = model.generate(
#     **inputs,
#     max_new_tokens=80,
#     do_sample=True,
#     temperature=0.7,
#     top_p=0.9,
#     eos_token_id=tokenizer.eos_token_id,
# )

# print(tokenizer.decode(output[0], skip_special_tokens=True))
