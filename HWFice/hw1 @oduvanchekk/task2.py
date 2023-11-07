"""щоб пересунути пірамідку з n — треба пересунути пірамідку з n-1, 
потім пересунути останній диск, а потім знов пересунути пірамідку з n-1
тобто  формула: f(x) = 2 * f(x-1) + 1, де f(x) це кількість пересувань
для переміщення пірамідки з х дисків"""


def best_moves():
    fx = 0
    for i in range(int(input("Input number of disks:\n"))):
        fx = 2 * fx + 1
    return fx


# print(best_moves())

"""завдяки цій програмі ми бачимо що по суті всі значення є якимось степенем двух, зменшеним на 1 (1, 3, 7, 15), тому 
можемо вивести формулу 2^n - 1, яку я точно взяв не з інету"""


print(2**int(input("Input number of disks:\n"))-1)
