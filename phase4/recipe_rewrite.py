import argparse
import os
import random
from itertools import permutations

dic = {}
step = {}

def remove_duplicates_ordered(lst):
    seen = set()
    return [t for t in lst if not (t in seen or seen.add(t))]


def generate_deps_flow(base): #find connections by ID (just number without words)
    with open("deps.flow", "w") as deps:
        with open(f"flow_graph_corpus/r-100/{base}.flow", "r") as file:
            for line in file:
                arry = line.strip("\n").split(" ")
                if (arry[1] != arry[-2] or arry[0] != arry[-3]) and (arry[3] == 't' or arry[3] == 'd'):
                    deps.write(line)

def format_recipe_steps(base): #write sentences, each sentence one step
    steps = {}
    
    with open(f"flow_graph_corpus/r-100/{base}.list", "r") as file:
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

    return formatted_steps

def find_dep_steps(): #find steps(sentences) that are dependent
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
        if index+1 >= len(list_dep):
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
    
    return (one_move_permutations_with_chains(result), uniques)


def extract_numbers(input_tuple):
    result = []
    for item in input_tuple:
        if isinstance(item, tuple):  # Check if item is a tuple
            result.extend(extract_numbers(item))  # Recursively extract numbers
        else:
            result.append(item)  # If it's a number, add it to the result
    return result

# def one_move_permutations(lst): #only move one and only one step at a time
#     permutations = [lst[:]]  # include the original
#     n = len(lst)
    
#     for i in range(n):
#         for j in range(n):
#             if i != j:
#                 new_lst = lst[:]  # copy original
#                 elem = new_lst.pop(i)
#                 new_lst.insert(j, elem)
#                 permutations.append(new_lst)
    
#     return permutations
def one_move_permutations_with_chains(lst):
    permutation = []
    n = len(lst)
    
    # Find chain positions (they stay fixed)
    chain_indices = [i for i, x in enumerate(lst) if isinstance(x, tuple) and len(x) > 1]

    # Define zones: start and end positions of non-chain sections
    zones = []
    prev = 0
    for chain_index in chain_indices:
        zones.append((prev, chain_index))
        prev = chain_index + 1
    zones.append((prev, n))  # after the last chain

    # print(f"Zones: {zones}")

    # For each zone
    for start, end in zones:
        zone = lst[start:end]
        # print(f"Processing zone: {zone}")

        if len(zone) <= 1:
            # print(" -> Skipping (not enough elements)")
            continue

        # Move one number at a time within the zone
        for i in range(len(zone)):
            for j in range(len(zone)):
                if i != j:
                    new_zone = zone[:]
                    elem = new_zone.pop(i)
                    new_zone.insert(j, elem)

                    # reconstruct the full list
                    new_lst = lst[:start] + new_zone + lst[end:]
                    permutation.append(new_lst)
        # print(permutation)
        return permutation

def main():
    global dic, step
    # parser = argparse.ArgumentParser(description="Process recipe files")
    # parser.add_argument("filename", help="Base filename (without extension) inside 'permutations' folder")
    # args = parser.parse_args()

    #base = args.filename
    
    files = [f'{x.split(".")[0]}' for x in os.listdir("flow_graph_corpus/r-100") if x.endswith(".list")]
    files.sort()
    
    for base in files:
        dic = {}
        step = {}
        generate_deps_flow(base)
        format_recipe_steps(base)
        output2 = find_dep_steps()
        output3, uniques = move_elements(output2, len(step))
        if output3 is None:
            output3 = []

        n = 0
        with open(f"permutations/{base}.txt", "w") as file:
            file.write("========\n")
            for i in range(1, len(step) + 1):
                file.write(f"{i}. {step[i]}\n")
            if len(uniques) > 1:
                random_elements = random.sample(uniques, 2)
                random_elements.sort()
                file.write(f"must step {random_elements[0]} happen before step {random_elements[1]}?\n")

            for out in output3:
                file.write("========\n")
                n += 1
                index = 1
                mapping = {}
                for key in extract_numbers(out):
                    mapping[key] = index
                    file.write(f"{index}. {step[key]}\n")
                    index += 1

                if len(uniques) > 1:
                    shash = [mapping[random_elements[0]], mapping[random_elements[1]]]
                    shash.sort()
                    file.write(f"must step {shash[0]} happen before step {shash[1]}?\n")

            file.write("========\n")
            file.write(f"number of recipes: {n} and {output2}")

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
