import random
import keyboard as k


def gen_rand_date():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = 2023
    date = f"{day}.{month}.{year}"
    return date


def gen_rand_tel():
    operator = random.choice(["63", "93", "67", "98", "44", "66", "68", "96", "97"])
    middle = random.randint(100, 999)
    end1 = random.randint(10, 99)
    end2 = random.randint(10, 99)
    tel = f"+38(0{operator})-{middle}-{end1}-{end2}"
    return tel


def gen_rand_polis():
    let1 = random.choice(["A", "B", "C", "D", "E"])
    let2 = random.choice(["T", "Y", "K", "L", "M"])
    digits = random.randint(1000000, 9999999)
    polis = f"{let1}{let2}{digits}"
    return polis


def gen_rand_long_num():
    month = random.randint(1, 12)
    year = random.randint(0, 23)
    m = "0"
    if month < 10:
        m += str(month)
    else:
        m = str(month)
    y = "0"
    if year < 10:
        y += str(year)
    else:
        y = str(year)
    digits = random.randint(1000, 9999)
    ln = f"{digits}{m}{y} {m}.20{y}"
    return ln


generating = True

while generating:
    try:
        if k.is_pressed("esc"):
            generating = False
        elif k.is_pressed("d"):
            print(gen_rand_date())
        elif k.is_pressed("t"):
            print(gen_rand_tel())
        elif k.is_pressed("p"):
            print(gen_rand_polis())
        elif k.is_pressed("l"):
            print(gen_rand_long_num())
    finally:
        pass

