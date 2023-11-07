import numpy as np
import matplotlib.pyplot as plt


# Задані цільові функції
def f1(x):
    return 2 - 3 * x + x ** 3


def f2(x):
    return 16 - x ** 2


fs1 = 3
fs2 = 1

# Округлені кордони інтервалу
x_values = np.arange(2, 3.874, 0.001)

# Створення списків для збереження точок області Парето
pareto_points = []


# Обчислення значень цільових функцій та визначення області Парето
def find_Pareto():
    for x in x_values:
        point = (float('{:.4f}'.format(f1(x) / fs1)), float('{:.4f}'.format(f2(x) / fs2)))
        pareto_points.append(['{:.4f}'.format(x), point, max(point[0], point[1]), min(point[0], point[1])])
    my_min_in_max = [pareto_points[0][2], [0]]
    my_max_in_min = [pareto_points[0][3], [0]]

    for index in range(len(pareto_points)):
        print(pareto_points[index][1], pareto_points[index][0])
        if pareto_points[index][2] < my_min_in_max[0]:
            my_min_in_max[0] = pareto_points[index][2]
            my_min_in_max[1] = pareto_points[index][0]
        if pareto_points[index][3] > my_max_in_min[0]:
            my_max_in_min[0] = pareto_points[index][3]
            my_max_in_min[1] = pareto_points[index][0]
    return f"{my_min_in_max} {my_max_in_min}"


def do_plot():
    plt.figure(figsize=(7, 5), layout='constrained')
    plt.plot(x_values, [f1(x) for x in x_values])
    plt.plot(x_values, [f2(x) for x in x_values])
    plt.grid()
    plt.show()


print(find_Pareto())
do_plot()
