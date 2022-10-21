arr = [1, 3, 6, 2, 2, 0, 4, 5]
target = 5


def targeted_pairs(array, tg):
    pairs = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if array[i] + array[j] == tg:
                pairs.append([array[i], array[j]])
    return pairs


print(targeted_pairs(arr, target))
