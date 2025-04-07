import argparse
import os
import random
from itertools import permutations

dic = {}
step = {}

def remove_duplicates_ordered(lst):
    seen = set()
    return [t for t in lst if not (t in seen or seen.add(t))]


def generate_deps_flow(base):
    with open("deps.flow", "w") as deps:
        with open(f"permutations/{base}.flow", "r") as file:
            for line in file:
                arry = line.strip("\n").split(" ")
                if (arry[1] != arry[-2] or arry[0] != arry[-3]) and (arry[3] == 't' or arry[3] == 'd'):
                    deps.write(line)

def format_recipe_steps(base):
    steps = {}
    
    with open(f"permutations/{base}.list", "r") as file:
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

def move_elements(rules, N):
    result = []
    
    i = 1  # start from 1
    index = 0  # track position in tuples_list
    uniques = []
    
    while i <= N:
        if index < len(rules) and i in rules[index]:
            result.append(rules[index])  # add the tuple
            i = max(rules[index]) + 1  # move i past this tuple
            index += 1  # move to next tuple
        else:
            uniques.append(i)
            result.append((i,))  # add single-element tuple
            i += 1  # move to the next number

    return (list(permutations(result)), uniques)

def extract_numbers(input_tuple):
    result = []
    for item in input_tuple:
        if isinstance(item, tuple):  # Check if item is a tuple
            result.extend(extract_numbers(item))  # Recursively extract numbers
        else:
            result.append(item)  # If it's a number, add it to the result
    return result
 

def main():
    parser = argparse.ArgumentParser(description="Process recipe files")
    parser.add_argument("filename", help="Base filename (without extension) inside 'permutations' folder")
    args = parser.parse_args()

    base = args.filename

    generate_deps_flow(base)
    format_recipe_steps(base)
    output2 = find_dep_steps()
    output3, uniques = move_elements(output2, len(step))

    n = 0
    with open(f"permutations/{base}.txt", "w") as file:
        if len(uniques) > 1:
            random_elements = random.sample(uniques, 2)

        for out in output3:
            file.write("========\n")
            n += 1
            index = 1
            mapping = {}
            for key in extract_numbers(out):
                mapping[key] = index
                file.write(f"{key}. {index}. {step[key]}\n")
                index += 1

            if len(uniques) > 1:
                shash = [mapping[random_elements[0]], mapping[random_elements[1]]]
                shash.sort()
                file.write(f"must step {shash[0]} happen before step {shash[1]}?\n")

        file.write(f"\n number of recipes: {n} and {output2}")

if __name__ == "__main__":
    main()
                
# output = format_recipe_steps()
# output2 = find_dep_steps()
# output3, uniques = move_elements(output2, len(step))
# print(output2)
# # print(step)
# n = 0
# with open("permutations/Almon_and_apple_cake.txt", "w") as file:
#     if len(uniques) > 1:
#         random_elements = random.sample(uniques, 2)

#     for out in output3:
#         file.write("========\n")
        
#         n +=1
#         index = 1
#         mapping = {}
        
#         for key in extract_numbers(out):
#             mapping[key] = index
#             file.write(f"{key}. {index}. {step[key]}\n")
#             index += 1
        
#         if len(uniques) > 1:
#             shash = [mapping[random_elements[0]], mapping[random_elements[1]]]
#             shash.sort()
#             file.write(f"must step {shash[0]} happen before step {shash[1]}?\n")
#     file.write(f"\n number of recipes: {n} and {output2}")
