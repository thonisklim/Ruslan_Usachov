# Codewars Council
def combined_honor(arr, d):
    groups = len(arr) // d
    # додаю всі значення від і до і+groups
    return max(sum(arr[i::groups]) for i in range(groups))


array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
print(array[1::3])

# print(combined_honor([1, 5, 6, 3, 4, 2], 3))
# print(combined_honor([1, 1, 0], 1))
