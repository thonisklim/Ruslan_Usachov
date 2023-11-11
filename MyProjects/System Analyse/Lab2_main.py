import matplotlib.pyplot as plt
from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from plyer import filechooser
import numpy as np
from sklearn.preprocessing import minmax_scale

Config.set("graphics", "fullscreen", 0)  # "auto"
Config.write()


class Lab2App(App):
    x_table = []
    y_table = []
    normed_x = []   # normed by minmax_scale
    normed_y = []
    selection = []  # file selection
    n = [[], []]          # dimensions of variables
    all_p = []      # powers of polinoms for x1, x2, x3
    lambdas = []
    psis = []
    k_y = 1         #for what y we are finding values

    def build(self):
        return 0

    # choose X
    def file_chooser(self, variable_name):
        filechooser.open_file(on_selection=self.get_path)
        self.input_table(variable_name)

    def get_path(self, selection):
        self.selection = selection

    def change_error_message(self, message):
        self.root.ids.error_label.text = message

    def get_p_values(self, p_values):
        if self.x_table and self.y_table:
            try:
                self.all_p = np.array(p_values, int)
            except ValueError:
                self.change_error_message("Рекомендую заповнити всі ступені P числами")
                print("Рекомендую заповнити всі ступені P числами")

    def input_table(self, variable_name):
        if self.selection:
            print(self.selection)
            file = open(self.selection[0], 'r')
            first = True
            for line in file.read().split('\n'):
                list_line = line.replace(',', '.').split('\t')
                if line == '':
                    # we're skipping empty raw
                    pass
                elif first:
                    first = False
                    match variable_name:
                        case 'x':
                            if self.x_table:
                                self.x_table.clear()
                        case 'y':
                            if self.y_table:
                                self.y_table.clear()
                    dim = find_dimension(variable_name, list_line)
                    # user have to upload X first
                    if dim:
                        self.n[variable_name == 'y'] = dim
                        print(self.n)
                    else:
                        exit("wrong variable_name")
                        break
                else:
                    match variable_name:
                        case 'x':
                            self.x_table.append([float(list_line[i]) for i in range(1, len(list_line))])
                        case 'y':
                            self.y_table.append([float(list_line[i]) for i in range(1, len(list_line))])
                        case _:
                            exit("wrong variable_name")
                            break

    def start(self):
        if self.x_table == [] or self.y_table == []:
            self.change_error_message("Таблиці пусті, без даних нічого не спрацює")
            print("Не хочу працювати з пустими таблицями")
        elif len(self.all_p) < 3:
            pass
        elif len(self.x_table) != len(self.y_table):
            self.change_error_message("Таблиці мають неоднакову кількість рядків")
            print("А спрацювало б, якби кількість рядків у таблицях співпадала")
        else:
            self.change_error_message("Все чудово")
            self.processing()

    def processing(self):
        self.normed_x = minmax_scale(self.x_table)
        self.normed_y = minmax_scale(self.y_table)
        print(f"\nPolinom:{do_chebish_polinom(self.normed_x[0][0], self.all_p[0])}")
        # всі лямбди першим методом
        print(f"\nl:\n{self.find_lambdas_m1()}")
        for i in range(len(self.n[0])):
            self.lambdas.append(self.find_lambda_k_m2(i + 1))
        # self.lambdas = np.array(self.lambdas)
        print(f"\nlambdas method 2:\n{self.lambdas}")
        print(f"\n{self.find_psi()}")
        # print(f"\n{self.find_a(1, 1, 1)}")

        # print(f"\n{self.find_f(1, 1, 1)}")

    def find_lambdas_m1(self):
        all_p = self.all_p
        A = []
        # do_chebish_polinom(do_norm(self.x_table)[0][0], p1)
        for q in range(len(self.x_table)):
            a_line = []
            # k = 0 1 2
            for k in range(len(self.n[0])):
                pos_x = sum(self.n[0][i] for i in range(k - 1))
                dim_x = self.n[0][k]
                # j = 0 1
                for j in range(dim_x):
                    # p = 0 1 2
                    for p in range(all_p[k] + 1):
                        a_line.append(do_chebish_polinom(self.normed_x[q][j + pos_x], p))
            A.append(a_line)
        A = np.array(A)
        # lambdas for 1st Y (index = k_y)
        return do_conjugate_gradient(A, self.normed_y[:, self.k_y - 1])

    def find_lambda_k_m2(self, k):
        k = k - 1
        my_p = self.all_p[k]
        dim_x = self.n[0][k]
        A = []
        for q in range(len(self.x_table)):
            a_line = []
            # k = k
            pos_x = sum(self.n[0][i] for i in range(k - 1))
            # j = 0 1
            for j in range(dim_x):
                # p = 0 1 2
                for p in range(my_p + 1):
                    a_line.append(do_chebish_polinom(self.normed_x[q][j + pos_x], p))
            A.append(a_line)
        A = np.array(A)
        # TODO change self.k_y from interface
        lambda_k = do_conjugate_gradient(A, self.normed_y[:, self.k_y - 1])
        return lambda_k

    def find_psi(self):
        # k input = 1 ... k
        dim_x = self.n[0]
        sum_var = []
        text_out = []
        # q = 0 ... 39
        # x_k = 0 1 2
        for x_k in range(len(dim_x)):
            my_p = self.all_p[x_k]
            # j = 0 1
            for j in range(dim_x[x_k]):
                s_var = 0
                text_sum = ""
                # p = 0 1 2
                for p in range(my_p + 1):
                    # we take first raw in normed_x for calculating polinom
                    s_var += self.lambdas[x_k][p + j * my_p] * do_chebish_polinom(self.normed_x[0][x_k + j * my_p], p)
                    text_sum += f"{self.lambdas[x_k][p + j * my_p]} * T{p}+"
                text_sum = text_sum.replace('+-', ' - ').replace('+', ' + ')
                sum_var.append(s_var)
                text_out.append(text_sum[:-3])
        return [sum_var, text_out]

    def find_a(self, y_k, x_k, q):
        psi_sum = sum(self.find_psi()[0])
        return self.normed_y[q][y_k] / psi_sum

    def find_f(self, x_k, y_k, q):
        dim_x = self.n[0][x_k]
        a = self.find_a(x_k, y_k, q)
        psis = self.find_psi()[0]
        sum_j = 0
        for j in range(dim_x):
            sum_j += a * psis[j]
        return sum_j


def find_dimension(variable_name, list_line):
    print(list_line)
    n = [0]
    variable_name = variable_name.upper()
    i = 1
    # list_line[0] = 'q'
    if len(list_line[1]) <= 2:
        n[0] = len(list_line) - 1
        return n
    for item in list_line:
        if item == 'q':
            pass
        elif f"{variable_name}{i}" in item:
            n[i - 1] += 1
        else:
            n.append(1)
            i += 1
    return n


'''
def do_norm(origin_table):
    table = []
    for k in range(len(origin_table)):
        line = []
        for i in range(len(origin_table[0])):
            my_column = [float(raw[i]) for raw in origin_table]
            min_val = min(my_column)
            max_val = max(my_column)
            line.append(float('{:.4f}'.format((float(origin_table[k][i]) - min_val) / (max_val - min_val))))
        table.append(line)
    # не виводиться номер q
    return np.array(table, float)


def do_norm_raw(origin_table, dim_var):
    table = []
    for k in range(len(origin_table)):
        line = []
        for j in range(len(dim_var)):
            pos_x = sum(dim_var[i] for i in range(j - 1))
            min_val = min(origin_table[k])
            max_val = max(origin_table[k])
            line.append(float('{:.4f}'.format((float(origin_table[k][j + pos_x]) - min_val) / (max_val - min_val))))
        table.append(line)
    # не виводиться номер q
    return np.array(table, float)

def do_anti_norm(n_table):
    normed_table = copy.deepcopy(n_table)
    # we don't normalise q column
    for i in range(1, len(normed_table[0])):
        my_column = [float(raw[i]) for raw in normed_table]
        min_val = min(my_column)
        max_val = max(my_column)
        # print(i, min_val, max_val, my_column)
        for k in range(len(normed_table)):
            normed_table[k][i] = float('{:.4f}'.format((float(normed_table[k][i]) * (max_val - min_val) + min_val)))
    return normed_table'''


def do_chebish_polinom(x, n):
    T = 0
    match n:
        case 0:
            T = 1
        case 1:
            T = -1 + 2 * x
        case _:
            T = 2 * (-1 + 2 * x) * do_chebish_polinom(x, n - 1) - do_chebish_polinom(x, n - 2)
    return T


def do_lezhandr_polinom(x, n):
    P = 0
    if n == 0:
        P = 1
    elif n == 1:
        P = x
    else:
        P = ((2 * n + 1) * x * do_lezhandr_polinom(x, n - 1) - n * do_lezhandr_polinom(x, n - 2)) * (1 / (n + 1))
    return P


def do_lagerr_polinom(x, n):
    L = 0
    if n == 0:
        L = 1
    elif n == 1:
        L = -x + 1
    else:
        L = ((2 * n + 1 - x) * do_lagerr_polinom(x, n - 1) - n ** 2 * do_lagerr_polinom(x, n - 2)) / (n + 1)
    return L


def do_ermit_polinom(x, n):
    H = 0
    if n == 0:
        H = 1
    elif n == 1:
        H = 2 * x
    else:
        H = 2 * x * do_ermit_polinom(x, n - 1) - 2 * n * do_ermit_polinom(x, n - 2)
    return H


def do_conjugate_gradient(a0, b0):
    a0 = np.array(a0)
    # b0 = np.array([((min(line) + max(line)) / 2) for line in b0])
    # b0 = np.array([line[0] for line in b0])
    A = np.dot(a0.transpose(), a0)
    b = np.dot(a0.transpose(), b0)

    if len(a0) == 0 or len(A[0]) != len(b):
        raise ValueError("Невірні розмірності матриці A або вектора b.")

    x = np.zeros(np.shape(A)[0])
    d = np.zeros(np.shape(A)[0])
    g = np.dot(A, x) - b

    while np.linalg.norm(g) > 0.000001:
        g_prev = g
        g = np.dot(A, x) - b
        d = -g + np.dot(np.dot(g.transpose(), g) / np.dot(g_prev.transpose(), g_prev), d)
        s = np.dot(d.transpose(), g) / np.dot(np.dot(d.transpose(), A), d)
        x = x - np.dot(s, d)
    return x


def do_plot(x_values, y_values):
    plt.figure(figsize=(7, 5), layout='constrained')
    plt.plot(x_values, y_values)
    plt.grid()
    plt.show()


Lab2App().run()
