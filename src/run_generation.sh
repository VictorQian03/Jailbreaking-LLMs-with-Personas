export EXPERIMENT_NAME="persona_test"
export SYSTEM_PROMPT_PATH="data/persona_dataset/raw_persona_dataset/all_personas_raw.txt"
export USER_PROMPT_PATH="data/goal_dataset/raw_goal_dataset/raw_goals.txt"
export MODEL_ID="deepseek-ai/DeepSeek-R1"
export SAVE="results/$EXPERIMENT_NAME/"
export OUTPUT_FILE_NAME="test_output.json"
mkdir -p $SAVE
python src/generation.py --system_prompt_path $SYSTEM_PROMPT_PATH --user_prompt_path $USER_PROMPT_PATH --model_id $MODEL_ID --output_path $SAVE/$OUTPUT_FILE_NAME
