import numpy as np


# Задані цільові функції
def f1(x):
    return 10 + 2 * x + x ** 2


def f2(x):
    return 16 - 0.5 * x ** 2


fs1 = 5
fs2 = 7.5

step = 0.001
# Округлені кордони інтервалу
x_values = np.arange(1, 3+step, step)

# Створення списків для збереження точок області Парето
pareto_points = []


# Обчислення значень цільових функцій та визначення області Парето
def find_Pareto():
    for x in x_values:
        point = (float('{:.4f}'.format(f1(x) / fs1)), float('{:.4f}'.format(f2(x) / fs2)))
        pareto_points.append([float('{:.4f}'.format(x)), point, max(point[0], point[1]), min(point[0], point[1])])
    my_min_in_max = [pareto_points[0][0], pareto_points[0][2]]
    my_max_in_min = [pareto_points[0][0], pareto_points[0][3]]

    for index in range(len(pareto_points)):
        print(pareto_points[index][0], pareto_points[index][1], pareto_points[index][2], pareto_points[index][3])
        if pareto_points[index][2] < my_min_in_max[1]:
            my_min_in_max[1] = pareto_points[index][2]
            my_min_in_max[0] = pareto_points[index][0]
        if pareto_points[index][3] > my_max_in_min[1]:
            my_max_in_min[1] = pareto_points[index][3]
            my_max_in_min[0] = pareto_points[index][0]
    return f"{my_min_in_max} {my_max_in_min}"


print(find_Pareto())
