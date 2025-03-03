import json
import pandas as pd

def label_baseline_prompts(input_json_path, output_json_path):
    """
    Labels prompts in a JSON file as 'Baseline' if they start with the baseline phrase.
    """
    with open(input_json_path, 'r') as f:
        data = json.load(f)

    for entry in data:
        system_prompt = entry.get('system_prompt', '')
        if system_prompt.startswith("You are a helpful assistant"):
            entry['label'] = 'Baseline'
        elif 'scenario_type' in entry:
          entry['label'] = "Unknown"

    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=4)


def label_persona_prompts(persona_dataset_path, input_json_path, output_json_path):
    """
    Labels persona prompts in a JSON file based on a persona dataset CSV.
    """
    persona_df = pd.read_csv(persona_dataset_path)
    persona_dict = dict(zip(persona_df['description'], persona_df['label']))

    with open(input_json_path, 'r') as f:
        data = json.load(f)

    for entry in data:
        system_prompt = entry.get('system_prompt', '')
        label_found = False
        for description, label in persona_dict.items():
            if system_prompt.startswith(description):
                entry['label'] = label
                label_found = True
                break
        if not label_found:
            entry['label'] = "Unknown"

    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=4)

def label_scenario_prompts(scenario_dataset_path, input_path, output_path):
    """
    Labels persona prompts in a JSON file based on a persona dataset CSV.
    """
    scenario_df = pd.read_csv(scenario_dataset_path)
    scenario_dict = dict(zip(scenario_df['scenario'], scenario_df['label']))

    with open(input_path, 'r') as f:
        data = json.load(f)

    data_df = pd.DataFrame(data)

    for description, label in scenario_dict.items():
        data_df.loc[data_df['system_prompt'].str.contains(description), 'scenario_type'] = label

    with open(output_path, 'w') as f:
        data_df.to_json(f, orient='records', indent=4)

def main():
    persona_dataset_csv = './data/persona_dataset/persona_dataset.csv'
    scenario_dataset_csv = './data/scenario_dataset/raw_scenario_dataset/baseline_scenarios.csv'

    input_files = {
        'baseline': [
            ('./results/baseline_and_scenario/b_sc_add_goal.json', './results/baseline_and_scenario/b_sc_add_goal_labeled.json'),
            ('./results/scenario_new_goals/scenario_new_goals.json', './results/scenario_new_goals/b_sc_labeled.json'),
            ('./results/baseline_new_goals/baseline_new_goals.json', './results/baseline_new_goals/baseline_new_goals_labeled.json')
        ],
        'persona': [
            ('./results/persona_goal/b_p_add_goal.json', './results/persona_goal/b_p_add_goal_labeled.json')
        ],
        'scenario': [
            ('./results/scenario_new_goals/b_sc_labeled.json', './results/scenario_new_goals/b_sc_add_goal_labeled.json')
        ]
    }

    for model_type, file_pairs in input_files.items():
        for input_path, output_path in file_pairs:
            if model_type == 'baseline':
                label_baseline_prompts(input_path, output_path)
            elif model_type == 'persona':
                label_persona_prompts(persona_dataset_csv, input_path, output_path)
            elif model_type == 'scenario':
                label_scenario_prompts(scenario_dataset_csv, input_path, output_path)

    print("Labeling complete. Check output JSON files.")

if __name__ == "__main__":
    main()