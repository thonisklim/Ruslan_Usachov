def sort_string():
    your_number = input("Gimme numberrr:\n")
    new_string = ""
    for i in range(9, -1, -1):
        for digit in your_number:
            if int(digit) == i:
                new_string += digit
    return new_string


print(sort_string())
