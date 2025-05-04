import os
import json
import re
import google.generativeai as genai
import time
from datetime import datetime

# 1. Configure Gemini
genai.configure(api_key="AIzaSyD4TWYW506EJ7XgKw_OpWhOSKdWPs7POUQ")
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# 1.1 Read the daily requests number
USAGE_FILE = "prompt_usage.json"
PROMPT_LIMIT = 500

# Load prompt usage data
if os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "r", encoding="utf-8") as f:
        usage_data = json.load(f)
    last_date = usage_data.get("date")
    prompts_sent_today = usage_data.get("prompts_sent_today", 0)

    # Check if it's a new day
    today_str = datetime.now().strftime("%Y-%m-%d")
    if last_date != today_str:
        prompts_sent_today = 0  # reset for the new day
else:
    prompts_sent_today = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

# 2. Get filenames (without .txt)
folder = "permutations"
files = [os.path.splitext(x)[0] for x in os.listdir("2.5-flash-preview-04-17") if x.endswith(".json")]


# 3. Loop through each file
for filename in files:
    txt_path = os.path.join(folder, f"{filename}.txt")
    print(f"Processing {filename}.txt")

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    # Find permutations (after the first "========")
    rest = content.split("========", 2)
    if len(rest) < 2:
        print(f"[SKIPPED] No permutations found in {filename}")
        continue

    # Split the rest into permutation blocks
    first_recipe_block = rest[1].strip()
    permutation_blocks = [first_recipe_block]
    # Skip files that only have the original recipe
    if len(permutation_blocks) == 0:
        print(f"[SKIPPED] Only original recipe in {filename}")
        continue

    results = []

    ##
    # In this loop we are reading permutations of original recipe and use the model
    # to generate an answer based on a given prompt.
    # To avoid request limit error we are waiting 30s at the end of each loop.
    for block in permutation_blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # Last line is the question
        question_line = lines[-1].strip()
        permuted_steps = "\n".join(lines[:-1]).strip()

        # Extract step numbers from the question
        match = re.search(r"step\s+(\d+).*step\s+(\d+)", question_line, re.IGNORECASE)
        if match:
            i, j = match.groups()
        else:
            i, j = "?", "?"


        # Construct your prompt
        prompt = f"""
Given a goal, a procedure to achieve that goal and a question about the steps in the procedure,
you are required to answer the question in one sentence.

Goal: {filename}

Procedure:
{permuted_steps}


Must Step {i} happen before Step {j}? Select between yes or no

""".strip()
        print(prompt)

        try:
            prompts_sent_today += 1
            
            # Give the prompt to model and extract an answer
            response = model.generate_content(prompt)
            answer = response.text.strip()
            
        except Exception as e:
            print(e)
            answer = f"[ERROR] {str(e)}"
            # binary_answer = "[ERROR]"
            # why_answer = str(e)
            
        tmp = {
            "goal": filename,
            "permuted_recipe": permuted_steps,
            "question": question_line,
            "i": i,
            "j": j,
            "answer": answer,
        }
            
        json_path = os.path.join("orig-1.5-flash-8b", f"{filename}.json")

        # If file exists, load the existing list; otherwise, start a new one
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Append the new item
        data.append(tmp)

        # Write the full list back to the file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved: {filename}.json")
        
        # wait 30sec before next request
        time.sleep(10)
        
        # check the number of prompts
        if prompts_sent_today >= PROMPT_LIMIT:
            break
    
    # Save results
    # if results:
    #     json_path = os.path.join(folder, f"pro.{filename}.json")
    #     with open(json_path, "w", encoding="utf-8") as f:
    #         json.dump(results, f, indent=2, ensure_ascii=False)
    #     print(f"Saved: pro.{filename}.json")
    # else:
    #     print(f"[SKIPPED] No valid permutations in {filename}")

# Save updated prompt count
usage_data = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "prompts_sent_today": prompts_sent_today
}

with open(USAGE_FILE, "w", encoding="utf-8") as f:
    json.dump(usage_data, f, indent=2)
    print("Updated prompt usage log.")
