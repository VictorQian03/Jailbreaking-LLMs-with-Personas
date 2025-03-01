import os
import json
import re

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def identify_persona(system_prompt, curated_personas):
    """Identify persona type and trait from system prompt using curated personas."""
    persona_type = "baseline"
    persona_trait = "baseline"
    
    for persona in curated_personas:
        description_start = persona["description"].split('.')[0] + '.'
        
        if description_start in system_prompt:
            return persona["type"], persona["label"]
    
    return persona_type, persona_trait

def identify_scenario(system_prompt, scenario_templates):
    """Identify scenario type from system prompt."""
    scenario_type = "none"
    
    goodfaith_pattern = r"You have just checked in to volunteer"
    neutral_pattern = r"You walk into a coffee shop"
    adversarial_pattern = r"You are sitting in an abandoned building"
    
    if re.search(goodfaith_pattern, system_prompt, re.IGNORECASE):
        scenario_type = "goodfaith"
    elif re.search(neutral_pattern, system_prompt, re.IGNORECASE):
        scenario_type = "neutral"
    elif re.search(adversarial_pattern, system_prompt, re.IGNORECASE):
        scenario_type = "adversarial"
    
    return scenario_type

def merge_json_files(eval_dir, curated_personas_path, scenario_templates_path):
    curated_personas = load_json_file(curated_personas_path)
    scenario_templates = load_json_file(scenario_templates_path)
    
    subdirs = [d for d in os.listdir(eval_dir) if os.path.isdir(os.path.join(eval_dir, d))]
    
    for subdir in subdirs:
        subdir_path = os.path.join(eval_dir, subdir)
        cot_file_path = os.path.join(subdir_path, "test_output_labeled_cot.json")
        response_file_path = os.path.join(subdir_path, "test_output_labeled_response.json")
        
        if not (os.path.exists(cot_file_path) and os.path.exists(response_file_path)):
            print(f"Missing required files in {subdir_path}. Skipping...")
            continue
        
        with open(cot_file_path, 'r') as cot_file:
            cot_data = json.load(cot_file)
        
        with open(response_file_path, 'r') as response_file:
            response_data = json.load(response_file)
        
        if len(cot_data) != len(response_data):
            print(f"Files in {subdir_path} have different lengths. Skipping...")
            continue
        
        merged_data = []
        for cot_item, response_item in zip(cot_data, response_data):
            merged_item = cot_item.copy()
            
            harmful_flag_cot = merged_item.pop("harmful_completion_flag", "0")
            merged_item["harmful_completion_flag_cot"] = harmful_flag_cot
            
            merged_item["harmful_completion_flag_response"] = response_item.get("harmful_completion_flag", "0")
            
            system_prompt = merged_item.get("system_prompt", "")
            
            if subdir == "baseline_goal":
                persona_type = "baseline"
                persona_trait = "baseline"
                scenario_type = "none"
            else:
                persona_type, persona_trait = identify_persona(system_prompt, curated_personas)
                scenario_type = identify_scenario(system_prompt, scenario_templates)
            
            merged_item["persona_type"] = persona_type
            merged_item["persona_trait"] = persona_trait
            merged_item["scenario_type"] = scenario_type
            
            merged_data.append(merged_item)
        
        output_file_path = os.path.join(subdir_path, "test_output_merged.json")
        with open(output_file_path, 'w') as output_file:
            json.dump(merged_data, output_file, indent=4)
        
        print(f"Successfully merged files in {subdir_path}")

if __name__ == "__main__":
    eval_directory = "eval"
    curated_personas_path = "data/persona_dataset/curated_personas/curated_personas.json"
    scenario_templates_path = "src/scenario_templates.json"
    
    merge_json_files(eval_directory, curated_personas_path, scenario_templates_path)
    
    print("Merging process completed.")