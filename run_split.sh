export INPUT_DIR="results/persona_and_scenario/"
export INPUT_FILE="p_sc_add_goal.json"
export OUTPUT_DIR="eval/total_goals/persona_and_scenario"
export OUTPUT_FILE="test_output_split.json"
mkdir -p $OUTPUT_DIR
python src/cot_split.py --input_file $INPUT_DIR/$INPUT_FILE --output_file $OUTPUT_DIR/$OUTPUT_FILE