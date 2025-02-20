import os
import json
import pandas as pd
from together import Together
from dotenv import load_dotenv

def load_api_key():
    """Loads the TogetherAI API key from the .env file."""
    load_dotenv()
    api_key = os.getenv("TOGETHERAI_API_KEY")
    if not api_key:
        raise ValueError("TOGETHERAI_API_KEY not found in .env file")
    return api_key

def call_llm(prompt_text, model_name="deepseek-ai/DeepSeek-V3"):
    """Calls the TogetherAI API to generate text."""
    client = Together(api_key=load_api_key())
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=1024 
    )
    if not response.choices:
        raise ValueError(f"LLM returned an empty response.  Response object: {response}")
    return response.choices[0].message.content

def save_raw_data(data, filename):
    filepath = os.path.join("data", "persona_dataset", "raw_personas", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, "w") as f:
            if isinstance(data, str):
                f.write(data)
            else:
                json.dump(data, f, indent=4)
    except Exception as e:
        print("Could not save the file", e)
    
def load_raw_data(filename):
    """Loads raw persona data from a JSON file."""
    filepath = os.path.join("data", "persona_dataset", "raw_personas", filename)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {filepath}")
        return None
    
def save_curated_data(data, filename):
    filepath = os.path.join("data", "persona_dataset", "curated_personas", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, "w") as f:
            if filename.endswith(".json"):
                json.dump(data, f, indent=4)
            else:
                f.write(str(data))
    except Exception as e:
        print("Could not save the file", e)

def save_final_data(data, filename="persona_dataset.csv"):
    filepath = os.path.join("data", "persona_dataset", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
    except Exception as e:
        print("Could not save the file", e)

