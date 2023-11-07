def find_median_index(array):
    for index_num in range(len(array)):
        if sum(array[:index_num]) == sum(array[index_num + 1:]):
            return index_num
    return -1


print(find_median_index([1, 2, 3, 4, 3, 2, 1]))
print(find_median_index([1, 100, 50, -51, 1, 1]))
# print(find_median_index([2, 1, 1]))
