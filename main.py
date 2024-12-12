import os
import json
from glob import glob

# Path to the root folder
root_folder = "generated_answers"

# Target folder path
target_folder = os.path.join(root_folder, "gpt-4-0613", "test_must_why")

# List all JSONL files in the target folder
jsonl_files = glob(os.path.join(target_folder, "*.jsonl"))

# Load and process each JSONL file
data_list = []
for jsonl_file in jsonl_files:
    with open(jsonl_file, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())  # Load JSON data from each line
                data_list.append(data)  # Append to a list for analysis
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {jsonl_file}: {e}")

# Print summary of loaded data
print(f"Loaded {len(data_list)} JSON objects from {target_folder}")
