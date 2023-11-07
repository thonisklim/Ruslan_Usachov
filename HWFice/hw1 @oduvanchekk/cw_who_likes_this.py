def likes(names):
    print(len(names))
    return [f"no one likes this",
            f"{names[0]} likes this",
            f"{names[0]} and {names[1]} like this",
            f"{names[0]}, {names[1]} and {names[2]} like this"][0] if len(names) < 4 else f"{names[0]}, {names[1]} and {len(names) - 2} like this"


a = [' ', "a b a"]
a[-1] += ' '
print(a)
