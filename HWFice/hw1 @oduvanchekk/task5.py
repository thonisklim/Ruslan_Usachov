def check_nums():
    my_list = input("Input your string:\n")
    my_min = int(my_list.split(' ')[0])
    my_max = my_min

    for element in my_list.split(' '):
        if int(element) < my_min:
            my_min = int(element)
        if int(element) > my_max:
            my_max = int(element)

    return f"{my_min} {my_max}"


print(check_nums())

