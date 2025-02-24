import json
import pandas as pd
import os
from collections import defaultdict

def aggregate_persona_and_scenario_stats(input_file, output_dir):
    """
    Reads the persona+scenario test output JSON file, computes aggregate
    statistics by (persona_type, scenario_type) and (persona_label, scenario_type),
    and saves them as CSV files.
    """
    with open(input_file, 'r') as f:
        data = json.load(f)

    persona_type_scenario_results = defaultdict(lambda: {'total': 0, 'refusals': 0, 'harmful': 0})
    persona_label_scenario_results = defaultdict(lambda: {'total': 0, 'refusals': 0, 'harmful': 0})

    for entry in data:
        p_type = entry.get('persona_type', 'Unknown')
        p_label = entry.get('persona_label', 'Unknown')
        s_type = entry.get('scenario_type', 'Unknown')

        persona_type_scenario_results[(p_type, s_type)]['total'] += 1
        if entry.get('refusal_flag', False):
            persona_type_scenario_results[(p_type, s_type)]['refusals'] += 1
        if entry.get('harmful_completion_flag', False):
            persona_type_scenario_results[(p_type, s_type)]['harmful'] += 1

        persona_label_scenario_results[(p_label, s_type)]['total'] += 1
        if entry.get('refusal_flag', False):
            persona_label_scenario_results[(p_label, s_type)]['refusals'] += 1
        if entry.get('harmful_completion_flag', False):
            persona_label_scenario_results[(p_label, s_type)]['harmful'] += 1

    rows_type_scenario = []
    for (ptype, stype), stats in persona_type_scenario_results.items():
        total = stats['total']
        refusals = stats['refusals']
        harmful = stats['harmful']
        refusal_rate = (refusals / total) * 100 if total else 0
        harmful_rate = (harmful / total) * 100 if total else 0

        rows_type_scenario.append({
            'persona_type': ptype,
            'scenario_type': stype,
            'total_entries': total,
            'refusal_count': refusals,
            'harmful_count': harmful,
            'refusal_rate (%)': refusal_rate,
            'harmful_rate (%)': harmful_rate
        })

    df_persona_type_scenario = pd.DataFrame(rows_type_scenario)
    df_persona_type_scenario = df_persona_type_scenario.sort_values(by=['persona_type', 'scenario_type'])

    rows_label_scenario = []
    for (plabel, stype), stats in persona_label_scenario_results.items():
        total = stats['total']
        refusals = stats['refusals']
        harmful = stats['harmful']
        refusal_rate = (refusals / total) * 100 if total else 0
        harmful_rate = (harmful / total) * 100 if total else 0

        rows_label_scenario.append({
            'persona_label': plabel,
            'scenario_type': stype,
            'total_entries': total,
            'refusal_count': refusals,
            'harmful_count': harmful,
            'refusal_rate (%)': refusal_rate,
            'harmful_rate (%)': harmful_rate
        })

    df_persona_label_scenario = pd.DataFrame(rows_label_scenario)
    df_persona_label_scenario = df_persona_label_scenario.sort_values(by=['persona_label', 'scenario_type'])

    output_file_1 = os.path.join(output_dir, 'persona_type_scenario_results.csv')
    output_file_2 = os.path.join(output_dir, 'persona_label_scenario_results.csv')

    df_persona_type_scenario.to_csv(output_file_1, index=False)
    df_persona_label_scenario.to_csv(output_file_2, index=False)

    print(f"Saved persona_type + scenario results to: {output_file_1}")
    print(f"Saved persona_label + scenario results to: {output_file_2}")

def main():
    input_file = './results/persona_and_scenario/test_output_with_tags.json'
    output_dir = './results'
    os.makedirs(output_dir, exist_ok=True)

    aggregate_persona_and_scenario_stats(input_file, output_dir)

if __name__ == '__main__':
    main()