import json

input_path = "medical_instruction_input_output_200.jsonl"
output_path = "gpt2_training.txt"

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        item = json.loads(line)

        instruction = item["instruction"]
        question = item["input"]
        answer = item["output"]

        # GPT-2 likes simple question→answer text
        text = (
            f"Instruction: {instruction}\n"
            f"Question: {question}\n"
            f"Answer: {answer}\n\n"
        )

        outfile.write(text)

print("Saved cleaned dataset to gpt2_training.txt")
