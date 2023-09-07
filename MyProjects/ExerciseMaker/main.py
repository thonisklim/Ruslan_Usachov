import random

translation_pairs = []
stress_list = list("А́")
normal_list = list("АаЕеИиІіОоУуЯяЮюЇїЄє")
lists_to_compare = [[], []]

# 0 -separator
# 1 - list of wrong symbols
memory = ['', []]


# для коректної роботи між словами та знаками мають стояти пробіли
# приклад: Перукар - Hairdresser
# а між кожною парою слів має стояти ентер (\n)
def input_tr(new_sep):
    if new_sep:
        sep_inp = input("Please, input separator, like /, or - which used in text\n"
                        "input enter to use –\n")
        if sep_inp == '':
            sep_inp = '–'
        memory[0] = sep_inp
    tr_separator = memory[0]
    print("input your translations, they have to be written like \'a - b\'\nto end input you need to press enter,\n"
          "than write '.', and than press enter again")
    tr = ""
    while 1:
        a = input()
        if a == '.':
            break
        tr += a + '\n'
    for item in tr.split('\n'):
        if item == '':
            pass
        elif item.find(tr_separator) == -1:
            translation_pairs.append(item.split())
        else:
            translation_pairs.append(item.split(f" {tr_separator} "))


def do_border():
    print("\n-------------------------------------------------------------------------\n")


def remove_wrong(some_string, list_of_wrong_symbols):
    for symbol in list_of_wrong_symbols:
        while 1:
            remove_index = some_string.find(symbol)
            if remove_index != -1:
                some_string = some_string[:remove_index] + some_string[remove_index + 1:]
            else:
                break
    return some_string


def do_nicer(new_list):
    if new_list:
        memory[1] = list(input("Write without spaces what symbols you want me to remove?\n"))
    for i in range(len(translation_pairs)):
        for k in range(len(translation_pairs[i])):
            translation_pairs[i][k] = remove_wrong(translation_pairs[i][k], memory[1])
            translation_pairs[i][k] = remove_wrong(translation_pairs[i][k], stress_list[1])


def nice_out():
    for item in translation_pairs:
        print(f"{item[0]} – {item[1]}")


def do_match_exercises():
    tr_nums = list(range(0, len(translation_pairs)))
    while len(tr_nums) >= 4:
        rand_tr_nums = []
        for i in range(4):
            a = random.choice(tr_nums)
            rand_tr_nums.append(a)
            tr_nums.remove(a)

        abcd = list(range(0, 4))
        random.shuffle(abcd)
        print(f"Match translations:\n"
              f"\ta. {translation_pairs[rand_tr_nums[0]][0]} {translation_pairs[rand_tr_nums[abcd[0]]][1]}\n"
              f"\tb. {translation_pairs[rand_tr_nums[1]][0]} {translation_pairs[rand_tr_nums[abcd[1]]][1]}\n"
              f"\tc. {translation_pairs[rand_tr_nums[2]][0]} {translation_pairs[rand_tr_nums[abcd[2]]][1]}\n"
              f"\td. {translation_pairs[rand_tr_nums[3]][0]} {translation_pairs[rand_tr_nums[abcd[3]]][1]}")


def do_write_ua_to_en_exercises():
    tr_nums = list(range(0, len(translation_pairs)))
    while len(tr_nums) >= 4:
        rand_tr_nums = []
        for i in range(4):
            a = random.choice(tr_nums)
            rand_tr_nums.append(a)
            tr_nums.remove(a)

        print(f"Write translations:\n"
              f"\ta. {translation_pairs[rand_tr_nums[0]][0]} ___ ({translation_pairs[rand_tr_nums[0]][1]})\n"
              f"\tb. {translation_pairs[rand_tr_nums[1]][0]} ___ ({translation_pairs[rand_tr_nums[1]][1]})\n"
              f"\tc. {translation_pairs[rand_tr_nums[2]][0]} ___ ({translation_pairs[rand_tr_nums[2]][1]})\n"
              f"\td. {translation_pairs[rand_tr_nums[3]][0]} ___ ({translation_pairs[rand_tr_nums[3]][1]})")


def find_words_gender(word):
    gender = ""
    consonants = "бвгґджзйклмнпрстфхцчшщ"
    if consonants.find(word[-1]) != -1:
        gender = "M"
        print(gender)
    elif word[-1] == "а" or word[-1] == "я":
        if word[-1] == "я" and consonants.find(word[-2]) != -1 and word[-2] == word[-3]:
            gender = "N"
        else:
            gender = "F"
        print(gender)
    else:
        print("undefined gender of " + word)
    return gender


def add_gender():
    for i in range(len(translation_pairs)):
        translation_pairs[i].append(find_words_gender(translation_pairs[i][0]))


def do_exercises():
    do_border()
    do_match_exercises()
    do_border()
    do_write_ua_to_en_exercises()


def wanna_repeat():
    do_border()
    return input("Input 1 if you want to repeat with same formatting\n"
                 "Input 2 if you want to repeat but change formatting\n")


def main():
    while 1:
        do_border()
        print("Hi! How can I help you?\n"
              "print 0 to end the program\n"
              "print 1 to do some exercises with formatting\n"
              "print 2 to do some exercises without formatting\n"
              "print 3 to do just nice formatting\n")
        match input():
            # exit
            case '0':
                do_border()
                print("You`re welcome")
                break
            # exercises with formatting
            case '1':
                first_time = True
                while 1:
                    do_border()
                    input_tr(first_time)
                    do_nicer(first_time)
                    do_exercises()
                    translation_pairs.clear()
                    match wanna_repeat():
                        case '1':
                            first_time = False
                        case '2':
                            pass
                        case _:
                            break
            # exercises without formatting
            case '2':
                first_time = True
                while 1:
                    do_border()
                    input_tr(first_time)
                    do_exercises()
                    translation_pairs.clear()
                    match wanna_repeat():
                        case '1':
                            first_time = False
                        case '2':
                            pass
                        case _:
                            break
            # just nice formatting
            case '3':
                first_time = True
                while 1:
                    do_border()
                    input_tr(first_time)
                    do_nicer(first_time)
                    nice_out()
                    translation_pairs.clear()
                    match wanna_repeat():
                        case '1':
                            first_time = False
                        case '2':
                            pass
                        case _:
                            break

    '''
    find_words_gender("Вагання")'''


def input_bunch():
    num_bunch = 0
    while num_bunch < 2:
        print(f"input your {num_bunch + 1} bunch, they have to be written like \na\nb\nto end input you "
              f"need to press enter,\nthan write '.', and than press enter again")
        tr = ""
        while 1:
            a = input()
            if a == '.':
                break
            tr += a + '\n'
        for item in tr.split('\n'):
            if item == '':
                pass
            else:
                lists_to_compare[num_bunch].append(item)
        num_bunch += 1


def compare_bunches():
    for i in range(len(lists_to_compare[0])):
        print(f"{lists_to_compare[0][i]} – {lists_to_compare[1][i]}")


def do_compared_bunches():
    input_bunch()
    compare_bunches()


def do_test():
    a = "t, (((jjoso"
    b = ",("
    for x in b:
        a.remove(b)

do_compared_bunches()
# main()
# print(translation_pairs)
