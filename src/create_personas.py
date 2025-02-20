import json
import utils
import re
import os
from prompts import GENERATE_TRAIT_PROMPT, GENERATE_MOTIVATION_PROMPT, GENERATE_DOMAIN_PROMPT

def parse_raw_trait_output(raw_output):
    personas = []
    pattern = (
        r"(?:\d+\.\s*)?"        
        r"\**Trait:\s*(.*?)\**" 
        r"\s*\**Description:\**"
        r"\s*\**\"(.*?)\""      
    )
    matches = re.findall(pattern, raw_output, re.DOTALL)
    for trait, description in matches:
        personas.append({
            "type": "trait-based",
            "trait": trait.strip(),
            "description": description.strip()
        })
    return personas

def parse_raw_motivation_output(raw_output):
    personas = []
    pattern = (
        r"(?:\d+\.\s*)?"        
        r"\**Motivation:\s*(.*?)\**" 
        r"\s*\**Description:\**"
        r"\s*\**\"(.*?)\""      
    )
    matches = re.findall(pattern, raw_output, re.DOTALL)
    for motivation, description in matches:
        personas.append({
            "type": "motivation-based",
            "motivation": motivation.strip(),
            "description": description.strip()
        })
    return personas

def parse_raw_domain_output(raw_output):
    personas = []
    pattern = (
        r"(?:\d+\.\s*)?"        
        r"\**Domain:\s*(.*?)\**" 
        r"\s*\**Description:\**"
        r"\s*\**\"(.*?)\""      
    )
    matches = re.findall(pattern, raw_output, re.DOTALL)
    for domain, description in matches:
        personas.append({
            "type": "domain-specific",
            "domain": domain.strip(),
            "description": description.strip()
        })
    return personas

def generate_personas(template_file=None):
    """Generates persona descriptions using DeepSeek-V3."""
    if template_file is None:
        template_file = os.path.join(
            os.path.dirname(__file__), 
            "persona_templates.json"
        )
    
    with open(template_file, "r") as f:
        templates = json.load(f)

    all_personas = []

    for template in templates:
        persona_type = template["type"]
        print(f"Generating {persona_type} personas...")

        if persona_type == "trait-based":
            raw_output = utils.call_llm(GENERATE_TRAIT_PROMPT)
            utils.save_raw_data(raw_output, f"{persona_type}_raw.txt")
            personas = parse_raw_trait_output(raw_output)
            all_personas.extend(personas)

        elif persona_type == "motivation-based":
            raw_output = utils.call_llm(GENERATE_MOTIVATION_PROMPT)
            utils.save_raw_data(raw_output, f"{persona_type}_raw.txt")
            personas = parse_raw_motivation_output(raw_output)
            all_personas.extend(personas)

        elif persona_type == "domain-specific":
            raw_output = utils.call_llm(GENERATE_DOMAIN_PROMPT)
            utils.save_raw_data(raw_output, f"{persona_type}_raw.txt")
            personas = parse_raw_domain_output(raw_output)
            all_personas.extend(personas)

    return all_personas

def curate_personas(raw_personas):
    """Manually reviews and edits the generated personas."""
    curated_personas = []
    for persona in raw_personas:
        print("-" * 20)
        print(f"Type: {persona.get('type', 'N/A')}")  
        if "trait" in persona:
            print(f"Trait: {persona['trait']}")
        if "motivation" in persona:
            print(f"Motivation: {persona['motivation']}")
        if "domain" in persona:
            print(f"Domain: {persona['domain']}")
        print(f"Description:\n{persona['description']}")

        while True:
            action = input("Keep (k), Edit (e), or Discard (d)? ").lower()
            if action == "k":
                curated_personas.append(persona)
                break
            elif action == "e":
                new_description = input("Enter the edited description: ")
                persona['description'] = new_description
            elif action == "d":
                break  
            else:
                print("Invalid input. Please enter 'k', 'e', or 'd'.")
    return curated_personas

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
    # 1. Generate all personas
    raw_personas = generate_personas()
    # 2. Curate them interactively
    curated_personas = curate_personas(raw_personas)
    # 3. Unify them into a consistent format
    unified_personas = unify_personas(curated_personas)
    # 4. Save the curated JSON
    utils.save_curated_data(unified_personas, "curated_personas.json")
    # 5. Save final CSV
    utils.save_final_data(unified_personas, "persona_dataset.csv")
    print("Persona dataset saved to data/persona_dataset/persona_dataset.csv")

if __name__ == "__main__":
    main()

