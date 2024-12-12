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

BASE_PATH = "/Users/amirhossein/Documents/Asal.Projects/CaT-Bench/generated_answers/gpt-4-0613/test_must_why"
file_path = os.path.join(BASE_PATH, "nondependent_real_before_basic_binary.jsonl")
df = read_jsonl_to_dataframe(file_path)

#print(df.head())

unique_titles = df['title'].nunique()
#print(f"Number of unique titles: {unique_titles}") 

questions_per_title = df.groupby('title')['question_idx'].count()
#print("Questions per title:")
#print(questions_per_title) 

yes_answers = df[df['model_answer'] == 'Yes']
#print(yes_answers)

print(f"Total number of questions: {len(df)}")
print(f"Number of unexpected 'Yes' answers: {len(yes_answers)}")
print(f"Percentage of unexpected 'Yes' answers: {len(yes_answers) / len(df) * 100:.2f}%")

# Group by title and count unexpected "Yes" answers
yes_by_title = yes_answers.groupby('title')['model_answer'].count().sort_values(ascending=False)
#print("\nUnexpected 'Yes' answers by title:")
#print(yes_by_title)

# Analyze which step comparisons are most problematic
step_comparisons = yes_answers['binary_question'].value_counts()
print("\nMost common step comparisons with unexpected 'Yes' answers:")
print(step_comparisons.head())