import json
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def load_data(file_path):
    """Load JSON data into a pandas DataFrame."""
    return pd.read_json(file_path)

def compute_metrics(df):
    """Compute total count, harmful count, refusal count, HCR and RR."""
    total = len(df)
    harmful = df['harmful_completion_flag'].sum()
    refusal = df['refusal_flag'].sum()
    HCR = (harmful / total) * 100 if total > 0 else np.nan
    RR = (refusal / total) * 100 if total > 0 else np.nan
    return total, harmful, refusal, HCR, RR

def perform_chi2_test(baseline_count, baseline_non_count, persona_count, persona_non_count):
    """Perform a Chi-Squared test on a 2x2 contingency table."""
    table = [
        [baseline_count, baseline_non_count],
        [persona_count, persona_non_count]
    ]
    chi2, p, _, _ = chi2_contingency(table)
    return chi2, p

def main():
    # Either choose to keep the base model in test_output_with_persona.json or a separate file
    #baseline_file = "results/persona_test/test_output_baseline_annotated.json"
    persona_file = "results/persona_test/test_output_with_persona.json"
    
    #baseline_df = load_data(baseline_file)
    persona_df = load_data(persona_file)
    
    # Compute baseline metrics
    """
    baseline_total, baseline_harmful, baseline_refusal, baseline_HCR, baseline_RR = compute_metrics(baseline_df)
    print("Baseline Metrics:")
    print(f"  Total Prompts: {baseline_total}")
    print(f"  Harmful Completions: {baseline_harmful} ({baseline_HCR:.2f}%)")
    print(f"  Refusals: {baseline_refusal} ({baseline_RR:.2f}%)")
    print("-" * 50)
    """

    # Group persona data by persona label (you could also group by persona type)
    persona_groups = persona_df.groupby("persona_label")
    
    results = []
    print("Metrics for Persona-Based Outputs by Label:")
    for persona, group in persona_groups:
        persona_total, persona_harmful, persona_refusal, persona_HCR, persona_RR = compute_metrics(group)
        """
        # Compute absolute and relative changes with respect to baseline
        abs_HCR = persona_HCR - baseline_HCR
        abs_RR = persona_RR - baseline_RR
        rel_HCR = (abs_HCR / baseline_HCR) * 100 if baseline_HCR != 0 else np.nan
        rel_RR = (abs_RR / baseline_RR) * 100 if baseline_RR != 0 else np.nan
        
        # Prepare contingency tables for Chi-Squared tests
        # For harmful completions:
        baseline_non_harmful = baseline_total - baseline_harmful
        persona_non_harmful = persona_total - persona_harmful
        chi2_h, p_h = perform_chi2_test(baseline_harmful, baseline_non_harmful, persona_harmful, persona_non_harmful)
        
        # For refusals:
        baseline_non_refusal = baseline_total - baseline_refusal
        persona_non_refusal = persona_total - persona_refusal
        chi2_r, p_r = perform_chi2_test(baseline_refusal, baseline_non_refusal, persona_refusal, persona_non_refusal)
        """
        # Print out the metrics for the persona group
        print(f"Persona: {persona}")
        print(f"  Total Prompts: {persona_total}")
        print(f"  Harmful Completions: {persona_harmful} ({persona_HCR:.2f}%)")
        print(f"  Refusals: {persona_refusal} ({persona_RR:.2f}%)")

    print("\nAggregate Metrics by Persona Type:")
    type_groups = persona_df.groupby("persona_type")
    for ptype, group in type_groups:
        total, harmful, refusal, HCR, RR = compute_metrics(group)
        print(f"\nPersona Type: {ptype}")
        print(f"  Total Prompts: {total}")
        print(f"  Harmful Completions: {harmful} ({HCR:.2f}%)")
        print(f"  Refusals: {refusal} ({RR:.2f}%)")
        """
        print(f"  Absolute Change in HCR: {abs_HCR:.2f}%")
        print(f"  Relative Change in HCR: {rel_HCR:.2f}%")
        print(f"  Absolute Change in RR: {abs_RR:.2f}%")
        print(f"  Relative Change in RR: {rel_RR:.2f}%")
        print(f"  Chi-Squared (Harmful): chi2 = {chi2_h:.2f}, p-value = {p_h:.4f}")
        print(f"  Chi-Squared (Refusal): chi2 = {chi2_r:.2f}, p-value = {p_r:.4f}")
        print("-" * 50)
        
        results.append({
            "persona": persona,
            "total": persona_total,
            "harmful_count": persona_harmful,
            "HCR": persona_HCR,
            "refusal_count": persona_refusal,
            "RR": persona_RR,
            "abs_HCR": abs_HCR,
            "rel_HCR": rel_HCR,
            "abs_RR": abs_RR,
            "rel_RR": rel_RR,
            "chi2_harmful": chi2_h,
            "p_value_harmful": p_h,
            "chi2_refusal": chi2_r,
            "p_value_refusal": p_r,
        })
        """
    """
    results_df = pd.DataFrame(results)
    output_csv = "results/persona_test/metrics_comparison.csv"
    results_df.to_csv(output_csv, index=False)
    print(f"Comparison metrics saved to: {output_csv}")
    """

if __name__ == "__main__":
    main()