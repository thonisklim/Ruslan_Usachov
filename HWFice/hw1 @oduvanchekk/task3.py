def find_nb(m):
    my_sum = 0
    n = 0
    while my_sum < m:
        my_sum += n ** 3
        if my_sum == m:
            return n
        n += 1
    else:
        return -1


# 1071225
# 100
print(find_nb(91716553919377))
