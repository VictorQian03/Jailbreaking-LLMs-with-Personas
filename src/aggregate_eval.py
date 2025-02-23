import json
import pandas as pd
from collections import defaultdict
import os

def aggregate_results(input_files, output_dir):
    """
    Aggregates refusal and harmful completion rates, creating separate tables for persona vs. baseline
    and scenario vs. baseline comparisons.
    """
    results = defaultdict(lambda: {
        'total': 0,
        'refusals': 0,
        'harmful': 0,
        'type': None  
    })

    for file_path in input_files:
        with open(file_path, 'r') as f:
            data = json.load(f)

        for entry in data:
            label = entry.get('label', 'Unknown')
            scenario_type = entry.get('scenario_type', None)

            if scenario_type is not None:
                key = scenario_type  
                results[key]['type'] = 'scenario'
            else:
                key = label 
                results[key]['type'] = 'persona'

            results[key]['total'] += 1
            if entry.get('refusal_flag', False) == True:
                results[key]['refusals'] += 1
            if entry.get('harmful_completion_flag', False) == True:
                results[key]['harmful'] += 1

    persona_data = []
    scenario_data = []

    for key, counts in results.items():
        total = counts['total']
        refusals = counts['refusals']
        harmful = counts['harmful']
        type_ = counts['type']

        refusal_rate = (refusals / total) * 100 if total > 0 else 0
        harmful_rate = (harmful / total) * 100 if total > 0 else 0

        data_entry = {
            'key': key, 
            'total_entries': total,
            'refusal_count': refusals,
            'harmful_count': harmful,
            'refusal_rate (%)': refusal_rate,
            'harmful_rate (%)': harmful_rate
        }
        if type_ == 'persona':
            persona_data.append(data_entry)
        elif type_ == 'scenario':
            scenario_data.append(data_entry)

    df_persona = pd.DataFrame(persona_data)
    df_scenario = pd.DataFrame(scenario_data)
    
    if 'Baseline' not in df_scenario['key'].values and 'Baseline' in df_persona['key'].values:
        baseline_persona_row = df_persona[df_persona['key'] == 'Baseline'].copy()
        baseline_persona_row = baseline_persona_row.drop(columns=['refusal_rate_diff (%)', 'harmful_rate_diff (%)'],
                                                         errors='ignore')
        df_scenario = pd.concat([df_scenario, baseline_persona_row], ignore_index=True)

    if 'Baseline' in df_persona['key'].values:
        baseline_row = df_persona[df_persona['key'] == 'Baseline'].iloc[0]
        baseline_refusal_rate = baseline_row['refusal_rate (%)']
        baseline_harmful_rate = baseline_row['harmful_rate (%)']

        df_persona['refusal_rate_diff (%)'] = df_persona['refusal_rate (%)'] - baseline_refusal_rate
        df_persona['harmful_rate_diff (%)'] = df_persona['harmful_rate (%)'] - baseline_harmful_rate
    else:
        df_persona['refusal_rate_diff (%)'] = None
        df_persona['harmful_rate_diff (%)'] = None

    if 'Baseline' in df_scenario['key'].values :
        baseline_row = df_scenario[df_scenario['key'] == 'Baseline'].iloc[0]
        baseline_refusal_rate = baseline_row['refusal_rate (%)']
        baseline_harmful_rate = baseline_row['harmful_rate (%)']

        df_scenario['refusal_rate_diff (%)'] = df_scenario['refusal_rate (%)'] - baseline_refusal_rate
        df_scenario['harmful_rate_diff (%)'] = df_scenario['harmful_rate (%)'] - baseline_harmful_rate

    else:
      df_scenario['refusal_rate_diff (%)'] = None
      df_scenario['harmful_rate_diff (%)'] = None

    df_persona = df_persona.sort_values(by=['key'])
    df_scenario = df_scenario.sort_values(by=['key'])

    persona_csv_path = os.path.join(output_dir, 'persona_results.csv')
    scenario_csv_path = os.path.join(output_dir, 'scenario_results.csv')

    df_persona.to_csv(persona_csv_path, index=False)
    df_scenario.to_csv(scenario_csv_path, index=False)

    print(f"Aggregated persona results saved to: {persona_csv_path}")
    print(f"Aggregated scenario results saved to: {scenario_csv_path}")

def main():
    input_files = [
        './results/baseline_goal/baseline_goal_evaluated.json',
        './results/baseline_and_scenario/b_sc_add_goal_evaluated.json',
        './results/persona_goal/b_p_add_goal_evaluated.json'
    ]

    output_dir = './results' 
    aggregate_results(input_files, output_dir)

if __name__ == "__main__":
    main()