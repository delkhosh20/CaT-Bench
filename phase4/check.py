steplist = input().split(" ")
with open("deps.flow", "r") as file:
    for line in file:
        arry = line.strip("\n").split(" ")
        if arry[1] == steplist[0]:
            print(line)
        if arry[-2] == steplist[0]:
            print(line)
        if arry[1] == steplist[1]:
            print(line)
        if arry[-2] == steplist[1]:
            print(line)

