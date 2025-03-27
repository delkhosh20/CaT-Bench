dic = {}
def format_recipe_steps():
    steps = {}
    
    with open("exp1.flow", "r") as file:
        for line in file:
            parts = line.strip("\n").split(" ")
            if len(parts) < 5:
                continue
            
            recipe_num, sentence_num, word_num, word, *rest = parts
            key = (recipe_num, sentence_num)
            if key not in steps:
                steps[key] = []
            
            steps[key].append(word)
        
    formatted_steps = []
    
    for i, (key, words) in enumerate(sorted(steps.items()), start=1):
        dic[f"{key[0]} {key[1]}"] = i
        sentence = " ".join(words).replace(' .', '.')
        formatted_steps.append(f"{i}. {sentence}")
    
    return "\n".join(formatted_steps)

list_dep = []
def find_dep_steps():
    with open("deps.flow", "r") as file:
        for line in file:
            listID = line.strip("\n").split(" ")
            strid = f"{listID[0]} {listID[1]}"
            strid2 = f"{listID[-3]} {listID[-2]}"
            list_dep.append((dic[strid], dic[strid2]))

            
# Example usage
# data = """(Your input data here)"""
output = format_recipe_steps()
output2 = find_dep_steps()
print(output)
print(dic)
print(list_dep)