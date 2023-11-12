import matplotlib.pyplot as plt
from kivy import Config
from kivy.app import App
from plyer import filechooser
import numpy as np
from sklearn.preprocessing import minmax_scale
from tkinter import filedialog

Config.set("graphics", "fullscreen", 0)  # "auto"
Config.write()


class Lab2App(App):
    selection = []  # file selection

    x_table = []
    y_table = []
    normed_x = []   # normed by minmax_scale
    normed_y = []
    n = [[], []]    # dimensions of variables
    all_p = []      # powers of polinoms for x1, x2, x3
    k_y = 1         # for what Y we are finding values
    k_pol = 1       # what type of the polinome we are using

    lambdas = []
    psi_table = []
    a_values = []
    f_table = []
    c_values = []
    main_f_table = []
    approximation = 0

    def build(self):
        return 0

    def reset_tables(self):
        self.normed_x = []
        self.normed_y = []
        self.lambdas = []
        self.psi_table = []
        self.a_values = []
        self.f_table = []
        self.c_values = []
        self.main_f_table = []

    # choose X
    def file_chooser(self, variable_name):
        filechooser.open_file(on_selection=self.get_path)
        self.input_table(variable_name)

    def file_saver(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        filechooser.save_file(on_selection=self.get_path)

    def get_path(self, selection):
        self.selection = selection

    def choose_polinome(self, k):
        self.k_pol = k

    def change_error_message(self, message):
        self.root.ids.error_label.text = message

    def get_values(self, p_values, i_y):
        if i_y:
            try:
                if 0 < int(i_y) <= len(self.y_table) + 1:
                    self.k_y = int(i_y)
            except ValueError:
                self.change_error_message("Без i_y нічого не спрацює")
        else:
            self.change_error_message("Не забув про i_y?")

        if len(self.x_table) and len(self.y_table):
            try:
                self.all_p = []
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
                    # clearing tables before input values in them
                    match variable_name:
                        case 'x':
                            self.x_table = []
                        case 'y':
                            self.y_table = []
                    dim = find_dimension(variable_name, list_line)
                    # defining dimensions of input tables
                    if dim:
                        self.n[variable_name == 'y'] = dim
                        print(self.n)
                    else:
                        exit("wrong variable_name")
                        break
                else:
                    # filling up the tables
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
            self.reset_tables()
            self.change_error_message("Все чудово")
            self.processing()

    def processing(self):
        self.x_table = np.array(self.x_table)
        self.y_table = np.array(self.y_table)
        self.normed_x = minmax_scale(self.x_table)
        self.normed_y = minmax_scale(self.y_table)
        # normed -> lambdas -> psi -> a -> F(x) -> c -> F(x1, x2, x3)
        for i in range(len(self.n[0])):
            self.lambdas.append(self.find_lambda_k_m2(i + 1))
        self.psi_table = self.find_psi()[0]
        self.a_values = self.find_a()
        self.f_table = self.find_f()
        self.c_values = self.find_c()
        self.main_f_table = self.find_main_f()
        # TODO input polinome k
        self.approximation = self.find_approximation()

        print(f"\nPolinom:{do_polinom(self.k_pol, self.normed_x[0][0], self.all_p[0])}")
        # всі лямбди першим методом
        print(f"\nl:\n{self.find_lambdas_m1()}")
        # self.lambdas = np.array(self.lambdas)
        print(f"\nlambdas method 2:\n{self.lambdas}")
        print(f"\n{self.psi_table}")
        print(f"\n{self.a_values}")
        print(f"\nf table{self.f_table}")
        print(f"\nc val = {self.c_values}")
        print(f"\nmain F = {self.main_f_table}")
        print(f"\napproximation = {self.approximation}")
        print(type(self.f_table))
        print(do_unnorm(self.f_table))
        self.do_plot()

    def do_plot(self):
        x_values = np.arange(0, len(self.x_table), 1)
        plt.figure(figsize=(7, 5), layout='constrained')
        plt.plot(x_values, self.main_f_table, label=f"Ф{self.k_y}(x1, x2, x3)")
        # plt.plot(x_values, self.y_table[:, self.k_y - 1], label=f"Y{self.k_y}")
        plt.plot(x_values, self.normed_y[:, self.k_y - 1], label=f"normed Y{self.k_y}")
        plt.text(0, 1.1, f"approx = {self.approximation}")
        plt.grid()
        plt.legend()
        plt.show()


    def find_lambdas_m1(self):
        all_p = self.all_p
        A = []
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
                        a_line.append(do_polinom(self.k_pol, self.normed_x[q][j + pos_x], p))
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
                    a_line.append(do_polinom(self.k_pol, self.normed_x[q][j + pos_x], p))
            A.append(a_line)
        A = np.array(A)
        lambda_k = do_conjugate_gradient(A, self.normed_y[:, self.k_y - 1])
        return lambda_k

    def find_psi(self):
        # k input = 1 ... k
        dim_x = self.n[0]
        sum_var = []
        text_out = []
        # q = 0 ... 39
        for q in range(len(self.normed_x)):
            line = []
            # x_k = 0 1 2
            for x_k in range(len(dim_x)):
                text_line = []
                my_p = self.all_p[x_k] + 1
                # j = 0 1
                for j in range(dim_x[x_k]):
                    s_var = 0
                    text_sum = ""
                    # p = 0 1 2
                    for p in range(my_p):
                        # we take first raw in normed_x for calculating polinom
                        a = self.lambdas[x_k][p + j * my_p]
                        s_var += a * do_polinom(self.k_pol, self.normed_x[q][x_k + j * dim_x[x_k]], p)
                        text_sum += f"{self.lambdas[x_k][p + j * my_p]} * T{p}(X{x_k + 1}{j + 1})+"
                    text_sum = text_sum.replace('+-', ' - ').replace('+', ' + ')
                    line.append(s_var)
                    text_line.append(f"PSIX{x_k + 1}{j + 1} = {text_sum[:-3]}")
                if q == 0:
                    text_out.append(text_line)
            sum_var.append(line)
        print(text_out)
        return [np.array(sum_var), text_out]

    def find_a(self):
        return do_conjugate_gradient(self.psi_table, self.normed_y[:, self.k_y - 1])

    def find_f(self):
        dim_x = self.n[0]
        f_table = []
        for q in range(len(self.psi_table)):
            line = []
            for x_k in range(len(dim_x)):
                pos_x = sum(self.n[0][i] for i in range(x_k - 1))
                line.append(sum(self.a_values[pos_x + j] * self.psi_table[q][pos_x + j] for j in range(dim_x[x_k])))
            f_table.append(line)
        return np.array(f_table)

    def find_c(self):
        return do_conjugate_gradient(self.f_table, self.normed_y[:, self.k_y - 1])

    def find_main_f(self):
        f_table = []
        for q in range(len(self.f_table)):
            f_table.append(sum(self.c_values[f_k] * self.f_table[q][f_k] for f_k in range(len(self.f_table[0]))))
        return np.array(f_table)

    def find_approximation(self):
        return max([abs(self.main_f_table[i] - self.normed_y[:, self.k_y - 1][i]) for i in range(len(self.normed_y))])

    def find_unnormed_f(self):
        table = []
        for q in range(len(self.f_table)):
            line = []
            for j in range(len(self.f_table[0])):
                my_column = self.f_table[:, j]
                line.append(self.f_table[q][j] * (max(my_column) - min(my_column)) + min(my_column))
            table.append(line)
        return np.array(table)


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


def do_polinom(k_polinom, x, n):
    match k_polinom:
        case 1:
            return do_chebish_polinom(x, n)
        case 2:
            return do_lezhandr_polinom(x, n)
        case 3:
            return do_lagerr_polinom(x, n)
        case 4:
            return do_ermit_polinom(x, n)


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


def do_unnorm(origin_table):
    table = []
    if type(origin_table[0]) is np.ndarray:
        for q in range(len(origin_table)):
            line = []
            for j in range(len(origin_table[0])):
                my_column = origin_table[:, j]
                line.append(origin_table[q][j] * (max(my_column) - min(my_column)) + min(my_column))
            table.append(line)
    else:
        # if origin_table is not a table, but a list:
        for number in origin_table:
            table.append(number * (max(origin_table) - min(origin_table)) + min(origin_table))
    return np.array(table)


def do_conjugate_gradient(a0, b0):
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


Lab2App().run()
