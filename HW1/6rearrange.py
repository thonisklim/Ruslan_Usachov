n = 315


def rearrange(number):
    # num to list
    arr = []
    for x in str(number):
        arr.append(int(x))
    # finding digits to rearrange
    for i in range(len(arr) - 1, 0, -1):
        if arr[i - 1] < arr[i]:
            arr[i - 1], arr[i] = arr[i], arr[i - 1]
            return "".join(str(x) for x in arr)
    return -1


print(rearrange(n))