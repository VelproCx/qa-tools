for i in range(1, 10):
    for j in range(1, i + 1):
        result = i * j
        print(f"{i} * {j} = {result:2d}", end="  ")
    print()