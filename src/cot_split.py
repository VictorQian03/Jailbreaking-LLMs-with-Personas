import json
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, required=True)
parser.add_argument("--output_file", type=str, required=True)
args = parser.parse_args()

with open(args.input_file, "r") as f:
    data = json.load(f)
    new_data = []
    for item in data:
        # Extract the CoT part using regex
        cot_match = re.search(r'<think>(.*?)\n</think>\n\n', item["answer"], re.DOTALL)
        cot_content = cot_match.group(1).strip() if cot_match else ""
        
        # Get the response part (everything after </think>\n\n)
        response = re.sub(r'<think>.*?\n</think>\n\n', '', item["answer"], flags=re.DOTALL).strip()
        
        new_item = {
            "system_prompt": item["system_prompt"],
            "user_prompt": item["user_prompt"],
            "cot": cot_content,
            "response": response,
            "refusal_flag": None,
            "harmful_completion_flag": None,
            "answer": item["answer"]
        }
        new_data.append(new_item)

with open(args.output_file, "w") as f:
    json.dump(new_data, f, indent=4)

