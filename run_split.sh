export INPUT_DIR="results/pure_baseline/"
export INPUT_FILE="test_output.json"
export OUTPUT_DIR="eval/pure_baseline/"
export OUTPUT_FILE="test_output_split.json"
mkdir -p $OUTPUT_DIR
python src/cot_split.py --input_file $INPUT_DIR/$INPUT_FILE --output_file $OUTPUT_DIR/$OUTPUT_FILE