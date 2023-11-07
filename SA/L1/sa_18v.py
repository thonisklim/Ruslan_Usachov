import numpy as np


# Задані цільові функції
def f1(x):
    return x + 3 * x ** 2


def f2(x):
    return 5 + 14 * x


# Заданні обмеження
fs1 = 20
fs2 = 70

# Округлені кордони інтервалу
x1 = 0  # треба обрахувати
x2 = 0
x_values = np.arange(x1, x2, 0.001)

# Створення списку для збереження точок області Парето
pareto_points = []


# Обчислення значень цільових функцій та визначення області Парето
def find_Pareto():
    for x in x_values:
        point = (float('{:.4f}'.format(f1(x) / fs1)), float('{:.4f}'.format(f2(x) / fs2)))
        pareto_points.append(['{:.4f}'.format(x), point, max(point[0], point[1]), min(point[0], point[1])])
    my_min_in_max = [pareto_points[0][2], pareto_points[0][0]]
    my_max_in_min = [pareto_points[0][3], pareto_points[0][0]]

    for index in range(len(pareto_points)):
        print(pareto_points[index][1], pareto_points[index][0])

        if pareto_points[index][2] < my_min_in_max[0]:
            my_min_in_max[0] = pareto_points[index][2]
            my_min_in_max[1] = pareto_points[index][0]

        if pareto_points[index][3] > my_max_in_min[0]:
            my_max_in_min[0] = pareto_points[index][3]
            my_max_in_min[1] = pareto_points[index][0]
    return f"{my_min_in_max} {my_max_in_min}"


print(find_Pareto())
