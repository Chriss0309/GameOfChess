def append_sum(lst):
    while len(lst) <= 6:
        result = lst[-1] + lst[-2]
        lst.append(result)
    return lst


print(append_sum([1, 1, 2]))
