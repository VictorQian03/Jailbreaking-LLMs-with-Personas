# Setup Instructions

## Persona generation

From the root directory, run the following command
``` python src/create_personas.py ```

## Scenario Concatenation

From the root directory, run the following command
``` python src/create_scenarios.py ```
You may also specify the specific persona/scenario files to use.

``` python src/create_scenarios.py <scenario_filepath> <persona_filepath>```

Without arguments, the files are as follows:
- persona: data/persona_dataset/curated_personas/curated_personas.json
- scenario: src/scenario_templates.json

## Data Organization

Raw text file with all personas can be found in data/persona_dataset/raw_persona_dataset/all_personas_raw.txt

Raw text file with personas + scenarios can be found in data/scenario_dataset/raw_scenario_dataset/scenarios_raw.txt