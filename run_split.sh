export INPUT_DIR="results/baseline_and_scenario"
export INPUT_FILE="b_sc_test_output.json"
export OUTPUT_DIR="eval/baseline_and_scenario/"
export OUTPUT_FILE="test_output_split.json"
mkdir -p $OUTPUT_DIR
python3 src/cot_split.py --input_file $INPUT_DIR/$INPUT_FILE --output_file $OUTPUT_DIR/$OUTPUT_FILE