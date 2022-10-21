lst = [1, 2, 'aabb', 65, 4]


def filter_list(s):
    new_list = []
    for i in s:
        if type(i) != str:
            new_list.append(i)
    return new_list


print(filter_list(lst))
