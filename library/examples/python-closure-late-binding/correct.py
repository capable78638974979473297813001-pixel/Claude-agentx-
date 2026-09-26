def multipliers(count):
    funcs = []
    for i in range(count):
        funcs.append(lambda i=i: i)
    return funcs
