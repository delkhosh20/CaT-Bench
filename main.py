import json
import os
import pandas as pd

# Function to read a JSONL file and convert it into a DataFrame
def read_jsonl_to_dataframe(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))  # Parse each line as JSON
    return pd.DataFrame(data)  # Convert to DataFrame

# Base folder paths
BASE_PATH = "/Users/amirhossein/Documents/Asal.Projects/CaT-Bench/generated_answers/gpt-4-0613/test_must_why"
OUTPUT_FOLDER = os.path.join(BASE_PATH, "analysis_results")

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Iterate through all JSONL files in the folder
for file_name in os.listdir(BASE_PATH):
    if file_name.endswith(".jsonl"):
        file_path = os.path.join(BASE_PATH, file_name)
        output_path = os.path.join(OUTPUT_FOLDER, file_name.replace(".jsonl", ""))

        # Create subfolder for each JSONL file's analysis
        os.makedirs(output_path, exist_ok=True)

        # Process the JSONL file
        df = read_jsonl_to_dataframe(file_path)

        # Export full DataFrame to CSV
        df.to_csv(os.path.join(output_path, "full_data.csv"), index=False)

        # Analyze unique titles
        questions_per_title = df.groupby('title')['question_idx'].count()

        # Export questions per title to CSV
        questions_per_title.to_csv(os.path.join(output_path, "questions_per_title.csv"), header=["Questions Count"])

        # Filter unexpected "Yes" answers
        yes_answers = df[df['model_answer'] == 'Yes']
        yes_answers.to_csv(os.path.join(output_path, "unexpected_yes_answers.csv"), index=False)

        # Total stats
        total_questions = len(df)
        unexpected_yes_count = len(yes_answers)
        unexpected_yes_percentage = unexpected_yes_count / total_questions * 100

        # Save stats to a summary CSV
        summary = pd.DataFrame({
            "Metric": ["Total Questions", "Unexpected 'Yes' Count", "Unexpected 'Yes' Percentage"],
            "Value": [total_questions, unexpected_yes_count, f"{unexpected_yes_percentage:.2f}%"]
        })
        summary.to_csv(os.path.join(output_path, "summary_stats.csv"), index=False)

        # Analyze 'Yes' by title
        yes_by_title = yes_answers.groupby('title')['model_answer'].count().sort_values(ascending=False)
        total_questions_per_title = df.groupby('title')['question_idx'].count()
        yes_percentage_by_title = (yes_by_title / total_questions_per_title * 100).sort_values(ascending=False)

        # Export title-level analysis to CSV
        yes_percentage_by_title.to_csv(os.path.join(output_path, "yes_percentage_by_title.csv"), header=["Yes Percentage"])

        # Analyze step comparisons with unexpected 'Yes' answers
        step_comparisons = yes_answers['binary_question'].value_counts()

        # Export step comparisons to CSV
        step_comparisons.to_csv(os.path.join(output_path, "step_comparisons.csv"), header=["Count"])

print(f"Analysis completed. Results are saved in: {OUTPUT_FOLDER}")

# Combine all full_data.csv files into one master file
combined_df = pd.DataFrame()
for folder in os.listdir(OUTPUT_FOLDER):
    subfolder_path = os.path.join(OUTPUT_FOLDER, folder)
    full_data_path = os.path.join(subfolder_path, "full_data.csv")
    if os.path.exists(full_data_path):
        temp_df = pd.read_csv(full_data_path)
        temp_df['source_file'] = folder  # Add source file column
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

combined_df.to_csv(os.path.join(OUTPUT_FOLDER, "combined_full_data.csv"), index=False)
