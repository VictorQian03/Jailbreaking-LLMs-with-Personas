import json
import re
import os
import sys
import pandas as pd
import utils
from pathlib import Path

def generate_goal_df(num_prompts=20, goal_file=None):
    if goal_file is None:
        goal_file = os.path.join(
            Path(__file__).resolve().parent.parent,
            "data/goal_dataset/goals.csv"
        )

    # Grab first num_prompts goals from file
    df = pd.read_csv(goal_file)
    goals_rows = df['goal'].head(num_prompts)


    # Save raw goals separated by newlines to txt file
    goals = goals_rows.to_numpy()
    trunc_goals = "\n".join(goals)
    filename = "raw_goals"
    utils.save_raw_data(trunc_goals, filename + ".txt", label="goal")

    # Save new pd df to csv
    filepath = os.path.join("data", "goal_dataset", filename + ".csv")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        df = pd.DataFrame(goals_rows)
        df.to_csv(filepath, index=False)
    except Exception as e:
        print("Could not save the csv", e)


    return goals_rows
        
    
def main():
    generate_goal_df()


if __name__ == "__main__":
    main()