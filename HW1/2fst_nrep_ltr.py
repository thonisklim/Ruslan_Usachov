word = "giggling"


def find_nrp_ltr(a):
    for x in a:
        if a.count(x) == 1:
            return x
    return -1


print(find_nrp_ltr(word))