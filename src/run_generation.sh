export EXPERIMENT_NAME="persona_and_scenario"
export SYSTEM_PROMPT_PATH="src/test_sys.txt"
export USER_PROMPT_PATH="src/test_user.txt"
export MODEL_ID="deepseek-ai/DeepSeek-V3"
export SAVE="results/$EXPERIMENT_NAME/"
export OUTPUT_FILE_NAME="test_output.json"
mkdir -p $SAVE
python src/generation.py --system_prompt_path $SYSTEM_PROMPT_PATH --user_prompt_path $USER_PROMPT_PATH --model_id $MODEL_ID --output_path $SAVE/$OUTPUT_FILE_NAME
