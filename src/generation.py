import os
import time
import json
import pandas as pd
from together import Together
import argparse
from tqdm import tqdm
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--model_id", type=str, required=True, default="deepseek-ai/DeepSeek-V3")
parser.add_argument("--system_prompt_path", type=str, required=True)
parser.add_argument("--user_prompt_path", type=str, required=True)
parser.add_argument("--output_path", type=str, required=True)
args = parser.parse_args()

load_dotenv()
api_key = os.getenv("TOGETHERAI_API_KEY")
if not api_key:
    raise ValueError("TOGETHERAI_API_KEY not found in .env file")

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
        max_tokens=100 
    )
    if not response.choices:
        raise ValueError(f"LLM returned an empty response.  Response object: {response}")
    answer = response.choices[0].message.content
    return answer

if __name__ == "__main__":

    sys_prompt_path = args.system_prompt_path
    user_prompt_path = args.user_prompt_path
    model_id = args.model_id
    output_path = args.output_path
    # Check file extensions
    if not sys_prompt_path.endswith('.txt'):
        print(f"Warning: System prompt file '{sys_prompt_path}' is not a .txt file")
    if not user_prompt_path.endswith('.txt'):
        print(f"Warning: User prompt file '{user_prompt_path}' is not a .txt file")

    with open(sys_prompt_path, "r") as f:
        sys_prompt_list = f.readlines()

    with open(user_prompt_path, "r") as f:
        user_prompt_list = f.readlines()
    
    time.sleep(50)
    
    generated_data = []
    total_iterations = len(sys_prompt_list) * len(user_prompt_list)
    with tqdm(total=total_iterations, desc="Generating responses") as pbar:
        for sys_prompt in sys_prompt_list:
            for user_prompt in user_prompt_list:
                answer = generate_text(model_id=model_id, system_prompt=sys_prompt, user_prompt=user_prompt)
                generated_data.append({
                    "system_prompt": sys_prompt,
                    "user_prompt": user_prompt,
                    "answer": answer
                })
                pbar.update(1)
                print(answer)
                time.sleep(50)

    with open(output_path, "w") as f:
        json.dump(generated_data, f, indent=4)