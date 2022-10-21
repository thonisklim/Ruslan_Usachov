n = 132189


def count_root(a):
    b = sum(int(x) for x in str(a))
    return b if b < 10 else count_root(b)


print(count_root(n))
