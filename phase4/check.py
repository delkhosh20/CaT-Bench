steplist = input("steps: ").split(" ")
with open("recipe.txt", "r") as file:
    recipe = file.read()

dic = {}
dic[steplist[0]] = []
dic[steplist[1]] = []
with open("deps.flow", "r") as file:
    for line in file:
        arry = line.strip("\n").split(" ")
        if arry[1] == steplist[0]:
            dic[steplist[0]].append(arry[-2])
        if arry[-2] == steplist[0]:
            dic[steplist[0]].append(arry[1])
        if arry[1] == steplist[1]:
            dic[steplist[1]].append(arry[-2])
        if arry[-2] == steplist[1]:
            dic[steplist[1]].append(arry[1])
print(dic)