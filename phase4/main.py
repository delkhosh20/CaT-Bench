with open("deps.flow", "w") as deps:
    with open("exp.flow", "r") as file:
        for line in file:
            arry = line.strip("\n").split(" ")
            if arry[1] != arry[-2]:
                deps.write(line)

    