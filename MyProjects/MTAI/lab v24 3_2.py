
a = [1, 3, 3, 5, 5, 8, 8, 8, 9, 9]
b = [1, 2, 3, 3, 7, 9]
c = [2, 3, 8]

k = 0
for i in range(len(c)):
    while k < len(b):
        print(b[k], c[i])
        if b[k] > c[i]:
            print("break")
            break
        elif b[k] == c[i]:
            b.pop(k)
            print("popped", c[i])
        else:
            k += 1
print(b)

k = 0
for i in range(len(b)):
    while k < len(a):
        print(a[k], b[i])
        if a[k] > b[i]:
            print("break")
            break
        elif a[k] == b[i]:
            a.pop(k)
            print("popped", b[i])
        else:
            k += 1

print(a)
