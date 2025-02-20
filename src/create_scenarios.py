import json
import utils
import re
import os
import sys
from pathlib import Path

def generate_sys_prompt(scenario_file=None, persona_file=None):
    """Generates persona descriptions using given model."""
    with open(scenario_file, "r") as f:
        scenarios = json.load(f)

    with open(persona_file, "r") as f:
        personas = json.load(f)

    all_prompts = []
    raw_prompts = ""

    for scenario in scenarios:
        scenario_type = scenario["type"]
        scenario_prompt = scenario["prompt_structure"]
        print(f"Generating {scenario_type} prompts...")

        for persona in personas:
            type = persona["type"]
            label = persona["label"]
            persona_prompt = persona["description"]
            print(f"Generating {type} persona prompts + scenarios ...")
            # Concatenate scenario onto persona
            sys_prompt = persona_prompt + " " + scenario_prompt
            raw_prompts += sys_prompt + "\n"
            all_prompts.append({
                "type": type,
                "trait": label,
                "scenario": scenario_type,
                "prompt": sys_prompt
            })
    utils.save_raw_data(raw_prompts, "scenarios_raw.txt", "scenario_dataset")
    return all_prompts

def unify_personas(raw_personas):
    unified = []
    for p in raw_personas:
        new_p = {
            "type": p["type"],
            "description": p["description"]
        }
        if "trait" in p:
            new_p["label"] = p["trait"]
        elif "motivation" in p:
            new_p["label"] = p["motivation"]
        elif "domain" in p:
            new_p["label"] = p["domain"]
        else:
            new_p["label"] = "N/A"

        unified.append(new_p)

    return unified

def main():
    # parse args
    args = sys.argv
    if len(args) == 3:
        scenario_file = args[1]
        persona_file = args[2]
    else:
        scenario_file = os.path.join(os.path.dirname(__file__), 
                                     "scenario_templates.json")
        persona_file =  os.path.join(Path(__file__).resolve().parent.parent, 
                                     "data/persona_dataset/curated_personas/curated_personas.json")

    # 1. Concatenate scenarios onto personas
    concat = generate_sys_prompt(scenario_file=scenario_file, persona_file=persona_file)
    # 2. Save the scenarios dataset into JSON and CSV files
    utils.save_scenarios_data(concat, "scenario_dataset")
    print("Persona + scenario dataset saved to data/scenario_dataset/scenario_dataset.csv")

if __name__ == "__main__":
    main()

