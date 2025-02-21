import csv
import json

def load_persona_mapping(persona_csv_path):
    """
    Load the persona dataset from a CSV file.
    Returns a dictionary mapping persona description (system prompt) to its type and label.
    """
    mapping = {}
    with open(persona_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            description = row["description"].strip()
            mapping[description] = {
                "persona_type": row["type"].strip(),
                "persona_label": row["label"].strip()
            }
    return mapping

def main():
    test_output_path = "results/persona_test/test_output_annotated.json"
    persona_csv_path = "data/persona_dataset/persona_dataset.csv"
    updated_output_path = "results/persona_test/test_output_with_persona.json"

    persona_mapping = load_persona_mapping(persona_csv_path)

    with open(test_output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        sys_prompt = item["system_prompt"].strip()
        if sys_prompt in persona_mapping:
            item.update(persona_mapping[sys_prompt])
        else:
            print(f"Warning: No matching persona found for system prompt:\n{sys_prompt}")
            item.update({"persona_type": None, "persona_label": None})

    with open(updated_output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated file with persona info saved at: {updated_output_path}")

if __name__ == "__main__":
    main()