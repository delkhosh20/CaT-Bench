import os
import json
import re
import google.generativeai as genai
import time

# 1. Configure Gemini
genai.configure(api_key="AIzaSyCZSq1vrrvjRE-DCj1fzJXzUDuoVgbcitk")
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. Get filenames (without .txt)
folder = "permutations"
#files = [os.path.splitext(x)[0] for x in os.listdir(folder) if x.endswith(".txt")]
files = [
 'Almond_and_apple_cake_recipe__All_recipes_UK1',
 'Almost_no_fat_banana_bread_recipe__All_recipes_UK1',
 'Apple_Crumble_Pie_recipe__All_recipes_UK1',
 'Best_crispy_roast_potatoes_recipe__All_recipes_UK1',
 'Black_Bean_and_Sweetcorn_Salad_recipe__All_recipes_UK1',
 'Blackberry_preserve_recipe__All_recipes_UK1']
# 3. Loop through each file
for filename in files:
    txt_path = os.path.join(folder, f"{filename}.txt")
    print(f"Processing {filename}.txt")

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Extract the original recipe
    original_match = re.search(r"======== Original Recipe ========\s*(.*?)\s*========", content, re.DOTALL)
    if not original_match:
        print(f"[SKIPPED] No original recipe found in {filename}")
        continue

    original_recipe = original_match.group(1).strip()
    
    # Find permutations (after the first "========")
    rest = content.split("========", 2)
    if len(rest) < 3:
        print(f"[SKIPPED] No permutations found in {filename}")
        continue

    # Split the rest into permutation blocks
    permutation_blocks = rest[2].strip().split("========")

    # Skip files that only have the original recipe
    if len(permutation_blocks) == 0:
        print(f"[SKIPPED] Only original recipe in {filename}")
        continue

    results = []

    for block in permutation_blocks[1:]:
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
            response = model.generate_content(prompt)
            answer = response.text.strip()
            time.sleep(30)
        except Exception as e:
            answer = f"[ERROR] {str(e)}"
            print(e)
            time.sleep(30)

        results.append({
            "goal": filename,
            "original_recipe": original_recipe,
            "permuted_recipe": permuted_steps,
            "question": question_line,
            "i": i,
            "j": j,
            "answer": answer
        })
    
    # Save results
    if results:
        json_path = os.path.join(folder, f"{filename}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Saved: {filename}.json")
    else:
        print(f"[SKIPPED] No valid permutations in {filename}")
