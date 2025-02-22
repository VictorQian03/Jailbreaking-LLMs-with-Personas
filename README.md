# Setup Instructions

## Persona generation

From the root directory, run the following command

``` python src/create_personas.py ```

## Scenario Concatenation

From the root directory, run the following command, with scenario and persona file paths optional

``` python src/create_scenarios.py <scenario_filepath> <persona_filepath>```

Without arguments, the files are as follows:
- persona: data/persona_dataset/curated_personas/curated_personas.json
- scenario: src/scenario_templates.json

## Prompt Fetching

We sample the first n prompts from [AdvBench](https://github.com/llm-attacks/llm-attacks/blob/main/data/advbench/harmful_behaviors.csv). When n is unspecified, we default to the first 20:

``` python src/grab_goals.py <num_prompts> ```


## Data Organization

Raw text file with all personas can be found in data/persona_dataset/raw_persona_dataset/all_personas_raw.txt

Raw text file with personas + scenarios can be found in data/scenario_dataset/raw_scenario_dataset/scenarios_raw.txt

Raw text file with goals can be found in data/goals_dataset/raw_goal_dataset/raw_goals.txt

## Generating Results

From the root directory, run the bash script

``` ./src/run_generation.sh```

You may change env variables like:
- EXPERIMENT_NAME
- SYSTEM_PROMPT_PATH
- USER_PROMPT_PATH
- MODEL_ID="deepseek-ai/DeepSeek-R1"
- OUTPUT_FILE_NAME="test_output.json"

You can then annotate the results using manual_evaluation.py, with the input and output files specified like so:

``` python3 src/manual_evaluation.py <input_file> <output_file> ```

Then append the dataset info:

``` python3 src/append_dataset_info.py <dataset_csv> <label> <test_output_path> <output_file> ```

where test_output_path is the output file from the manual evaluation code, and label is either baseline, persona, or scenario.