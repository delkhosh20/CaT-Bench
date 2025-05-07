import re

def extract_original_answers(filepath):
    answers = {}
    with open(filepath, 'r') as f:
        content = f.read()

    blocks = content.strip().split("File: ")
    for block in blocks[1:]:
        lines = block.strip().split('\n')
        filename = lines[0].strip()
        goal = filename.replace('.json', '')

        correct_match = re.search(r"Correct\s+\(NO\)\s+answers:\s+(\d+)", block)
        total_match = re.search(r"Total questions:\s+(\d+)", block)

        if correct_match and total_match:
            correct = int(correct_match.group(1))
            total = int(total_match.group(1))

            if total == 1:
                original = 'no' if correct == 1 else 'yes'
                answers[goal] = original
            else:
                print(f"⚠️ Skipped '{goal}' — has multiple questions in original.")
    return answers


def compare_permutations(original_txt, permutations_txt):
    original_answers = extract_original_answers(original_txt)
    results = {}

    no_to_yes = []
    yes_to_no = []

    with open(permutations_txt, 'r') as f:
        content = f.read()

    blocks = content.strip().split("File: ")
    for block in blocks[1:]:
        lines = block.strip().split('\n')
        filename = lines[0].strip()
        goal = filename.replace('.json', '')

        if goal not in original_answers:
            continue
        
        original = original_answers[goal]
        permutations = re.findall(r"Answer:\s*(yes|no)", block, re.IGNORECASE)
        if original == 'no':
        #total = len(permutations)
            diffs = sum(1 for ans in permutations if ans.lower() != original)
        else:
            diff = re.search(r"Correct\s+\(NO\)\s+answers:\s+(\d+)", block)
            diffs = int(diff.group(1)) if diff else 0
            # Extract the total number of questions
        total_match = re.search(r"Total questions:\s*(\d+)", block)
        total = int(total_match.group(1)) if total_match else 0

        # Track for no->yes or yes->no switches
        # Find reported number of 'Correct (NO)' answers
        correct_match = re.search(r"Correct\s+\(NO\)\s+answers:\s+(\d+)", block)
        reported_correct_no = int(correct_match.group(1)) if correct_match else 0

        # Flip detection based on original and reported permutation accuracy
        if original == 'no' and reported_correct_no < total:
            no_to_yes.append(goal)
        elif original == 'yes' and reported_correct_no > 0:
            yes_to_no.append(goal)

        results[goal] = {
            "original": original,
            "total_permutations": total,
            "differing_answers": diffs,
        }

    return results, no_to_yes, yes_to_no


# === Run the comparison ===

original_txt_path = "orig-2.5-flash-preview-04-17.txt"      # update if needed
permutations_txt_path = "2.5-flash-preview-04-17.txt"

comparison, no_to_yes_list, yes_to_no_list = compare_permutations(original_txt_path, permutations_txt_path)

# === Write main comparison results ===
with open('comparison_gemini-2.5-flash.txt', 'w') as out:
    for goal, data in comparison.items():
        out.write(f"Recipe: {goal}\n")
        out.write(f"  Original answer: {data['original']}\n")
        out.write(f"  Total permutations: {data['total_permutations']}\n")
        out.write(f"  Differing answers: {data['differing_answers']}\n\n")

# === Write flipped answer lists ===
with open('no_to_yes_2.5flash.txt', 'w') as f:
    f.writelines(goal + '\n' for goal in no_to_yes_list)

with open('yes_to_no_2.5flash.txt', 'w') as f:
    f.writelines(goal + '\n' for goal in yes_to_no_list)
