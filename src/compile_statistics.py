import os
import json
import pandas as pd
import numpy as np
from collections import defaultdict
import re

def safe_int_conversion(value, default=0):
    """
    Safely convert a value to an integer, handling malformed strings.
    """
    if value is None:
        return default

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        match = re.search(r'\d+', value)
        if match:
            return int(match.group())

    return default

def compile_statistics(eval_dir):
    """
    Compile statistics on harmful completions and refusals across all merged files.
    Now correctly handles harmful_completion_flag_response as a discrete variable (0, 1, 2, 3).
    """
    stats_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {
        'count': 0,
        'harmful_cot_sum': 0,  
        'harmful_response_sum': 0, 
        'refusal_count': 0
    }))))

    subdirs = [d for d in os.listdir(eval_dir) if os.path.isdir(os.path.join(eval_dir, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(eval_dir, subdir)
        merged_file_path = os.path.join(subdir_path, "test_output_merged.json")

        if not os.path.exists(merged_file_path):
            print(f"Merged file not found in {subdir_path}. Skipping...")
            continue

        try:
            with open(merged_file_path, 'r') as merged_file:
                merged_data = json.load(merged_file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {merged_file_path}: {e}")
            continue

        for entry in merged_data:
            user_prompt = entry.get('user_prompt', '').strip()
            persona_type = entry.get('persona_type', 'unknown')
            persona_trait = entry.get('persona_trait', 'unknown')
            scenario_type = entry.get('scenario_type', 'unknown')

            harmful_cot = safe_int_conversion(entry.get('harmful_completion_flag_cot'))
            harmful_response = safe_int_conversion(entry.get('harmful_completion_flag_response'))
            refusal = safe_int_conversion(entry.get('refusal_flag'))

            stats_data[user_prompt][persona_type][persona_trait][scenario_type]['count'] += 1
            stats_data[user_prompt][persona_type][persona_trait][scenario_type]['harmful_cot_sum'] += harmful_cot
            stats_data[user_prompt][persona_type][persona_trait][scenario_type]['harmful_response_sum'] += harmful_response
            stats_data[user_prompt][persona_type][persona_trait][scenario_type]['refusal_count'] += refusal

    rows = []
    for prompt, prompt_data in stats_data.items():
        for p_type, type_data in prompt_data.items():
            for p_trait, trait_data in type_data.items():
                for s_type, counts in trait_data.items():
                    total = counts['count']
                    if total > 0:
                        harmful_cot_rate = (counts['harmful_cot_sum'] / total) * (100 / 3)
                        harmful_response_rate = (counts['harmful_response_sum'] / total) * (100 / 3)
                        refusal_rate = (counts['refusal_count'] / total) * 100  
                    else:
                        harmful_cot_rate = harmful_response_rate = refusal_rate = 0

                    rows.append({
                        'user_prompt': prompt,
                        'persona_type': p_type,
                        'persona_trait': p_trait,
                        'scenario_type': s_type,
                        'count': total,
                        'harmful_cot_sum': counts['harmful_cot_sum'],       
                        'harmful_response_sum': counts['harmful_response_sum'], 
                        'refusal_count': counts['refusal_count'],
                        'harmful_cot_rate': harmful_cot_rate,
                        'harmful_response_rate': harmful_response_rate,
                        'refusal_rate': refusal_rate
                    })

    stats_df = pd.DataFrame(rows)

    return stats_df


def compute_baseline_comparisons(stats_df):
    """
    Compute differences between each configuration and the baseline.
    """
    df = stats_df.copy()

    baseline_values = df[(df['persona_type'] == 'baseline') &
                         (df['persona_trait'] == 'baseline') &
                         (df['scenario_type'] == 'none')].copy()

    baseline_map = {}
    for _, row in baseline_values.iterrows():
        prompt = row['user_prompt']
        baseline_map[prompt] = {
            'baseline_harmful_cot_rate': row['harmful_cot_rate'],
            'baseline_harmful_response_rate': row['harmful_response_rate'],
            'baseline_refusal_rate': row['refusal_rate']
        }

    for prompt in df['user_prompt'].unique():
        if prompt in baseline_map:
            prompt_indices = df['user_prompt'] == prompt

            df.loc[prompt_indices, 'baseline_harmful_cot_rate'] = baseline_map[prompt]['baseline_harmful_cot_rate']
            df.loc[prompt_indices, 'baseline_harmful_response_rate'] = baseline_map[prompt]['baseline_harmful_response_rate']
            df.loc[prompt_indices, 'baseline_refusal_rate'] = baseline_map[prompt]['baseline_refusal_rate']

            df.loc[prompt_indices, 'abs_diff_harmful_cot'] = df.loc[prompt_indices, 'harmful_cot_rate'] - baseline_map[prompt]['baseline_harmful_cot_rate']
            df.loc[prompt_indices, 'abs_diff_harmful_response'] = df.loc[prompt_indices, 'harmful_response_rate'] - baseline_map[prompt]['baseline_harmful_response_rate']
            df.loc[prompt_indices, 'abs_diff_refusal'] = df.loc[prompt_indices, 'refusal_rate'] - baseline_map[prompt]['baseline_refusal_rate']

            for metric in ['harmful_cot_rate', 'harmful_response_rate', 'refusal_rate']:
                baseline_val = baseline_map[prompt][f'baseline_{metric}']
                if baseline_val != 0:
                    df.loc[prompt_indices, f'rel_diff_{metric.replace("_rate", "")}'] = (
                        (df.loc[prompt_indices, metric] - baseline_val) / baseline_val * 100
                    )
                else:
                    df.loc[prompt_indices, f'rel_diff_{metric.replace("_rate", "")}'] = np.nan

    return df

def generate_aggregations(df):
    """
    Generate aggregated statistics by different dimensions.
    """
    aggregated_dfs = {}

    agg_funcs = {
        'count': 'sum',
        'harmful_cot_rate': 'mean',
        'harmful_response_rate': 'mean',
        'refusal_rate': 'mean',
        'abs_diff_harmful_cot': 'mean',
        'abs_diff_harmful_response': 'mean',
        'abs_diff_refusal': 'mean',
        'harmful_cot_sum': 'sum',       
        'harmful_response_sum': 'sum'   

    }

    agg_persona_type = df.groupby('persona_type').agg(agg_funcs).reset_index()
    aggregated_dfs['by_persona_type'] = agg_persona_type

    agg_persona_trait = df.groupby(['persona_type', 'persona_trait']).agg(agg_funcs).reset_index()
    aggregated_dfs['by_persona_trait'] = agg_persona_trait

    agg_scenario_type = df.groupby('scenario_type').agg(agg_funcs).reset_index()
    aggregated_dfs['by_scenario_type'] = agg_scenario_type

    agg_persona_scenario = df.groupby(['persona_type', 'scenario_type']).agg(agg_funcs).reset_index()
    aggregated_dfs['by_persona_scenario'] = agg_persona_scenario

    agg_prompt = df.groupby('user_prompt').agg(agg_funcs).reset_index()
    aggregated_dfs['by_prompt'] = agg_prompt

    return aggregated_dfs

def validate_merged_files(eval_dir):
    """
    Validate the merged files to check for formatting issues.
    """
    problematic_files = []

    subdirs = [d for d in os.listdir(eval_dir) if os.path.isdir(os.path.join(eval_dir, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(eval_dir, subdir)
        merged_file_path = os.path.join(subdir_path, "test_output_merged.json")

        if not os.path.exists(merged_file_path):
            continue

        try:
            with open(merged_file_path, 'r') as merged_file:
                merged_data = json.load(merged_file)

            for i, entry in enumerate(merged_data[:5]):  
                try:
                    cot_flag = int(entry.get('harmful_completion_flag_cot', 0))
                    response_flag = int(entry.get('harmful_completion_flag_response', 0))
                    refusal_flag = int(entry.get('refusal_flag', 0))
                except (ValueError, TypeError):
                    problematic_files.append(f"{merged_file_path} (has malformed flag values)")
                    break

                if not (0 <= cot_flag <= 3 and 0 <= response_flag <= 3 and 0 <= refusal_flag <= 1):
                    problematic_files.append(f"{merged_file_path} (has malformed flag values)")
                    break

        except Exception as e:
            problematic_files.append(f"{merged_file_path} (Error: {str(e)})")

    return problematic_files

def main():
    eval_directory = "eval"
    output_directory = "statistics"

    print("Validating merged files...")
    problematic_files = validate_merged_files(eval_directory)

    if problematic_files:
        print("\nWarning: Issues detected in the following files:")
        for file in problematic_files:
            print(f"  - {file}")
        print("\nProceeding with analysis, but results may be affected.")

    os.makedirs(output_directory, exist_ok=True)

    print("Compiling statistics...")
    stats_df = compile_statistics(eval_directory)

    if stats_df.empty:
        print("No data found or all data was invalid. Please check your merged files.")
        return

    print("Computing baseline comparisons...")
    comparison_df = compute_baseline_comparisons(stats_df)

    comparison_df.to_csv(os.path.join(output_directory, "full_statistics.csv"), index=False)

    print("Generating aggregated statistics...")
    aggregated_dfs = generate_aggregations(comparison_df)

    for name, df in aggregated_dfs.items():
        df.to_csv(os.path.join(output_directory, f"{name}_statistics.csv"), index=False)

    print(f"Statistics saved to the '{output_directory}' directory.")

if __name__ == "__main__":
    main()