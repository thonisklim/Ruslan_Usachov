def is_anagram(x, y):
    if len(x) != len(y):
        return False
    for letter in x:
        if letter in y:
            y = y.replace(letter, '', 1)
        else:
            return False
    return True


def group_anagrams(arr):
    my_anagrams = []
    for word in arr:
        if len(my_anagrams) == 0:
            my_anagrams.append([word])
        else:
            for index in range(len(my_anagrams)):
                if is_anagram(word, my_anagrams[index][0]):
                    my_anagrams[index].append(word)
                    break
                elif index == len(my_anagrams) - 1:
                    my_anagrams.append([word])
                    break
    return my_anagrams


# print(group_anagrams(['ababab', 'bababa', 'nbnb']))
print(group_anagrams(["tsar", "rat", "tar", "star", "tars", "cheese"]))

