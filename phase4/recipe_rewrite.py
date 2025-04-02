from itertools import permutations

def remove_duplicates_ordered(lst):
    seen = set()
    return [t for t in lst if not (t in seen or seen.add(t))]

dic = {}
step = {}
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
        step[i] = sentence
        formatted_steps.append(f"{i}. {sentence}")
    
    return formatted_steps

def find_dep_steps():
    list_dep = []
    with open("deps.flow", "r") as file:
        for line in file:
            listID = line.strip("\n").split(" ")
            strid = f"{listID[0]} {listID[1]}"
            strid2 = f"{listID[-3]} {listID[-2]}"
            list_dep.append((dic[strid], dic[strid2]))
    
    list_dep = remove_duplicates_ordered(list_dep)
    
    index = 0
    while True:
        if index+1 == len(list_dep):
            break
        
        current = list_dep[index]
        next = list_dep[index+1]
        
        if current[-1] == next[0]:
            merged = current + next[1:]
            list_dep = list_dep[:index] + [merged] + list_dep[index+2:]
        else:
            index += 1
    
    return list_dep     

def move_elements(rules):
    rules = [(1), (2), (3)] + [rules[0]] + [(10)] + [rules[1]]
    return list(permutations(rules))

def extract_numbers(input_tuple):
    result = []
    for item in input_tuple:
        if isinstance(item, tuple):  # Check if item is a tuple
            result.extend(extract_numbers(item))  # Recursively extract numbers
        else:
            result.append(item)  # If it's a number, add it to the result
    return result
                
output = format_recipe_steps()
output2 = find_dep_steps()
output3 = move_elements(output2)
# print(output2)
# print(step)
n = 0
with open("Almond_and_apple_cake.txt", "w") as file:
    for out in output3:
        file.write("========\n")
        n +=1
        for key in extract_numbers(out):
            file.write(f"{key}. {step[key]}\n")
    file.write(f"\n number of recipes: {n}")
