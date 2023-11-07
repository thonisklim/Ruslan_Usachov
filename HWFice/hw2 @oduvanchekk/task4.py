# delicious sausages

def unpack_sausages(truck):
    my_sausages = ''
    my_reward = 0
    for box in truck:
        for package in box:
            if package[0] == '[' and package[-1] == ']':
                unpacked = package[1:-1]
                if len(unpacked) == 4 and len(set(unpacked)) == 1:
                    my_reward += 1
                    if my_reward % 5:
                        my_sausages += ''.join(unpacked)
    return ' '.join(my_sausages)


print(unpack_sausages([ [ "(-)", "[IIII]", "[))))]" ], [ "IuI", "[llll]" ], [ "[@@@@]", "UwU",
"[IlII]" ], [ "IuI", "[))))]", "x" ], [] ]))

