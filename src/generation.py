import os
import json
import pandas as pd
from together import Together
import argparse
from tqdm import tqdm
import time

parser = argparse.ArgumentParser()
parser.add_argument("--model_id", type=str, required=True, default="deepseek-ai/DeepSeek-R1")
parser.add_argument("--system_prompt_path", type=str, required=True)
parser.add_argument("--user_prompt_path", type=str, required=True)
parser.add_argument("--output_path", type=str, required=True)
args = parser.parse_args()

api_key = "d331c997ce653e6915f50a7ad394a8d3a5d3825e0eb99f086ff0166d4a3f8f63"
if api_key == "PASTE YOUR API KEY HERE":
    raise ValueError("Please replace the default API key with your actual Together API key")

def generate_text(model_id,system_prompt, user_prompt):
    """Calls the TogetherAI API to generate text."""
    client = Together(api_key=api_key)
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["# END"],
        max_tokens=1000 
    )
    if not response.choices:
        raise ValueError(f"LLM returned an empty response.  Response object: {response}")
    answer = response.choices[0].message.content
    return answer

if __name__ == "__main__":


    # sys_prompt_path = args.system_prompt_path
    user_prompt_path = args.user_prompt_path
    model_id = args.model_id
    output_path = args.output_path
    # Check file extensions
    # if not sys_prompt_path.endswith('.txt'):
    #     print(f"Warning: System prompt file '{sys_prompt_path}' is not a .txt file")
    if not user_prompt_path.endswith('.txt'):
        print(f"Warning: User prompt file '{user_prompt_path}' is not a .txt file")

    with open("data/scenario_dataset/baseline_s.json", "r") as f:
        sys_prompt_list = json.load(f)

    with open(user_prompt_path, "r") as f:
        user_prompt_list = f.readlines()
    
    
    
    generated_data = []
    total_iterations = len(sys_prompt_list) * len(user_prompt_list)
    with tqdm(total=total_iterations, desc="Generating responses") as pbar:
        for sys_prompt in sys_prompt_list:
            for user_prompt in user_prompt_list:
                answer = generate_text(model_id=model_id, system_prompt=sys_prompt["system_prompt"], user_prompt=user_prompt)
                current_data = {
                    "system_prompt": sys_prompt["system_prompt"],
                    "user_prompt": user_prompt,
                    "answer": answer,
                    "scenario_type": sys_prompt["scenario_type"]
                }
                generated_data.append(current_data)
                
                # Save after each generation and print confirmation
                with open(output_path, "w") as f:
                    json.dump(generated_data, f, indent=4)
                print(f"\nSaved {len(generated_data)} responses to {output_path}")
                
                pbar.update(1)
                time.sleep(50)

    # Final save is redundant but kept for clarity
    with open(output_path, "w") as f:
        json.dump(generated_data, f, indent=4)