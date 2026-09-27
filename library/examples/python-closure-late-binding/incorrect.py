def multipliers(count):
    funcs = []
    for i in range(count):
        funcs.append(lambda: i)
    return funcs
