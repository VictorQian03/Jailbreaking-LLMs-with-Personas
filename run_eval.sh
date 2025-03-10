export MODEL_ID="Qwen/QwQ-32B-Preview"
export PROMPT_TYPE="cot"

export INPUT_DIR="qwen_eval/baseline_and_scenario/"
export INPUT_FILE="test_output_split.json"
export OUTPUT_DIR="qwen_eval/baseline_and_scenario/"
export OUTPUT_FILE="test_output_labeled_cot.json"
python3 src/auto_eval_harmful.py --model_id $MODEL_ID --prompt_type $PROMPT_TYPE --input_path $INPUT_DIR/$INPUT_FILE --output_path $OUTPUT_DIR/$OUTPUT_FILE

