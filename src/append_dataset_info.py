import csv
import json
import sys

def load_mapping(dataset_csv_path, label="persona"):
    """
    Load the dataset from a CSV file.
    Returns a dictionary mapping description (system prompt) to its type and label.
    """
    mapping = {}
    with open(dataset_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if label == "persona":
            for row in reader:
                description = row["description"].strip()
                mapping[description] = {
                    "persona_type": row["type"].strip(),
                    "persona_label": row["label"].strip(),
                    "scenario_type": None
                }
        elif label == "scenario":
            for row in reader:
                description = row["prompt"].strip()
                print(description)
                mapping[description] = {
                    "persona_type": row["type"].strip(),
                    "persona_label": row["trait"].strip(),
                    "scenario_type": row["scenario"].strip()
                }
        elif label == "baseline":
            for row in reader:
                description = "You are a helpful AI assistant."
                mapping[description] = {
                    "persona_type": None,
                    "persona_label": None,
                    "scenario_type": None
                }
    return mapping

def main():
    args = sys.argv
    if len(args) == 5:
        csv_path = args[1]
        label = args[2]
        test_output_path = args[3]
        updated_output_path = args[4]
    else:
        csv_path = "data/persona_dataset/persona_dataset.csv"
        label = "persona"
        test_output_path = "results/persona_test/test_output_annotated.json"
        updated_output_path = "results/persona_test/test_output_with_persona.json"

    mapping = load_mapping(csv_path, label)

    with open(test_output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n")

    for item in data:
        sys_prompt = item["system_prompt"].strip()
        if sys_prompt in mapping or label == "baseline":
            print(sys_prompt)
            item.update(mapping[sys_prompt])
        else:
            print(f"Warning: No matching persona found for system prompt:\n{sys_prompt}")
            item.update({"persona_type": None, "persona_label": None})

    with open(updated_output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated file with persona info saved at: {updated_output_path}")

if __name__ == "__main__":
    main()