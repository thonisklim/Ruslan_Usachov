print("Enter key\n")
inp = int(input())
# base 2 to 10
a = 0
i = 0
while inp > 0:
    a += (inp % 10)*2**i
    inp //= 10
    i += 1
# base 10 to 3
b = ''
while a > 0:
    b += str(a % 3)
    a //= 3
# reverse str
c = ''
for i in reversed(b):
    c += i
print(c)
