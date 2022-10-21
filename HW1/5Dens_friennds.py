s = "Fired:Corwill;Wilfred:Corwill;Barney:TornBull;Betty:Tornbull;Bjon:Tornbull;Raphael:Corwill;Alfred:Corwill";


def take_second(e):
    return e[1]


# тут список отримує зручніший для програми вигляд
def do_better_list(meh):
    meh = meh.upper()
    lst = meh.split(";")
    betterlst = []
    for i in range(len(lst)):
        betterlst.append(lst[i].split(":"))
    return betterlst


def sort_by_last_name(fixedlst):
    # спочатку список сортується по іменам, потім по фаміліям, завдяки key=takeSecond
    return sorted(sorted(fixedlst), key=take_second)


print(sort_by_last_name(do_better_list(s)))
