from math import sqrt


def is_prime(num):
    num = int(num)
    if num <= 1:
        return False
    i = 2
    while i <= sqrt(num):
        if num % i == 0:
            return False
        i += 1
    return True


print(is_prime(int(input("Input number:\n"))))

