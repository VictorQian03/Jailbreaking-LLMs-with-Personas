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

Raw text file with goals can be found in data/goal_dataset/raw_goal_dataset/raw_goals.txt