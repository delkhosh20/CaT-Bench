with open("deps.flow", "w") as deps:
    with open("permutations/Almon_and_apple_cake.flow", "r") as file:
        for line in file:
            arry = line.strip("\n").split(" ")
            if (arry[1] != arry[-2] or arry[0] != arry[-3]) and (arry[3] == 't' or arry[3] == 'd'):
                deps.write(line)

    