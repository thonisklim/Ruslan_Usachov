import numpy as np
import matplotlib.pyplot as plt


def f12(x1, x2):
    return -5*x1**2 + 2*x1 + 3*x2


def f21(x1, x2):
    return -2*x2**2 + x1**2 + 30


def delta_i(f, fs):
    return np.abs(f - fs)


step = 0.02
x1_values = np.arange(0, 2+step, step)
x2_values = np.arange(1, 4+step, step)

f12_result = {}
f12_points = {}

f21_result = {}
f21_points = {}

delta_points = []


def find_max_min():
    for x1 in x1_values:
        arr = {}
        for x2 in x2_values:
            arr[float('{:.4f}'.format(f12(x1, x2)))] = [float('{:.4f}'.format(x1)), float('{:.4f}'.format(x2))]
        min_key = min([key for key in arr])
        f12_points[min_key] = arr.get(min_key)
        print(arr.get(min_key), min_key)
    max_key = max([key for key in f12_points])
    f12_result[max_key] = f12_points.get(max_key)
    print('\n')

    for x2 in x2_values:
        arr = {}
        for x1 in x1_values:
            arr[float('{:.4f}'.format(f21(x1, x2)))] = [float('{:.4f}'.format(x1)), float('{:.4f}'.format(x2))]
        min_key = min([key for key in arr])
        f21_points[min_key] = arr.get(min_key)
        print(arr.get(min_key), min_key)
    max_key = max([key for key in f21_points])
    f21_result[max_key] = f21_points.get(max_key)
    print('\n')


def find_delta1():
    f12_d_i = {}
    f21_d_i = {}
    delta = []
    for x1 in x1_values:
        for x2 in x2_values:
            coordinates = (float('{:.4f}'.format(x1)), float('{:.4f}'.format(x2)))
            f12_d_i[coordinates] = float('{:.4f}'.format(delta_i(f12(x1, x2), list(f12_result.keys())[0])))
            f21_d_i[coordinates] = float('{:.4f}'.format(delta_i(f21(x1, x2), list(f21_result.keys())[0])))
            print(f"{f12_d_i[coordinates]} {f21_d_i[coordinates]} ({float('{:.4f}'.format(x1)), float('{:.4f}'.format(x2))})")
            # if delta_i(f12(x1, x2), list(f12_result.keys())[0]) == delta_i(f21(x1, x2), list(f21_result.keys())[0]):
            #     delta.append((x1, x2))

    min_f21 = {}
    min_val_f12 = min(f12_d_i.values())
    for item in f12_d_i:
        if f12_d_i[item] == min_val_f12:
            min_f21[item] = f21_d_i.get(item)
    min_val_f21 = min(min_f21.values())
    for item in min_f21:
        if f21_d_i[item] == min_val_f21:
            delta.append(item)
    return delta


def find_delta():
    for x1 in x1_values:
        for x2 in x2_values:
            coordinates = (float('{:.4f}'.format(x1)), float('{:.4f}'.format(x2)))
            f12_d_i = float('{:.4f}'.format(delta_i(f12(x1, x2), list(f12_result.keys())[0])))
            f21_d_i = float('{:.4f}'.format(delta_i(f21(x1, x2), list(f21_result.keys())[0])))
            delta_points.append([coordinates, f12_d_i, f21_d_i, max(f12_d_i, f21_d_i)])
    my_min_in_max = [delta_points[0][0], delta_points[0][3]]

    for index in range(len(delta_points)):
        if delta_points[index][3] < my_min_in_max[1]:
            my_min_in_max[1] = delta_points[index][3]
            my_min_in_max[0] = delta_points[index][0]

    delta = []
    for index in range(len(delta_points)):
        if delta_points[index][3] == my_min_in_max[1]:
            delta.append([delta_points[index][0], delta_points[index][3]])
    return delta


def do_plot():
    plt.figure(figsize=(7, 5))
    for x1 in x1_values:
        plt.plot([x2 for x2 in x2_values], [f12(x1, x2) for x2 in x2_values], label=f"f12({float('{:.4f}'.format(x1))}, x2)")
    plt.grid()
    plt.legend()
    plt.figure(figsize=(7, 5))
    for x2 in x2_values:
        plt.plot([x1 for x1 in x1_values], [f21(x1, x2) for x1 in x1_values], label=f"f21(x1, {float('{:.4f}'.format(x2))})")
    plt.grid()
    plt.legend()
    plt.show()


find_max_min()
do_plot()
# print(f12_points, '\n', f21_points)
print(f12_result, '\n', f21_result)
print(find_delta())
