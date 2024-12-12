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
file_path = os.path.join(BASE_PATH, "dependent_fake_after_basic_binary.jsonl")
df = read_jsonl_to_dataframe(file_path)

print(df.head())  # Display the first few rows of the DataFrame