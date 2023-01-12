print("Enter key\n")
a = int(input(), 2)
# base 10 to 3
b = ''
while a > 0:
    b += str(a % 3)
    a //= 3
print(b[::-1])
