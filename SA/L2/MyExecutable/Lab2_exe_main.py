import os
import matplotlib.pyplot as plt
import cj_gradient as cj
import polinomes as pol
import numpy as np
import sympy as sp
from collections.abc import Iterable
from sklearn.preprocessing import minmax_scale
from tkinter import filedialog


def do_first_line(var_name, dim):
    if len(dim) == 1:
        return "q    " + "    ".join([f"{var_name}{i+1}" for i in range(dim[0])]) + '\n'
    else:
        return "q   " + "   ".join([f"{var_name}{i+1}{j+1}" for i in range(len(dim)) for j in range(dim[i])]) + '\n'


def format_table(table):
    formatted_table = ""
    if isinstance(table[0], Iterable):
        q = 1
        for row in table:
            formatted_row = [f"{q}    "]
            for item in row:
                if isinstance(item, (int, float)):
                    formatted_item = "{:.3f}".format(item)
                else:
                    formatted_item = str(item)
                formatted_row.append(formatted_item)
            formatted_table += "   ".join(formatted_row) + "\n"
            q += 1
    else:
        formatted_row = []
        for item in table:
            if isinstance(item, (int, float)):
                formatted_item = "{:.3f}".format(item)
            else:
                formatted_item = str(item)
            formatted_row.append(formatted_item)
        formatted_table += "   ".join(formatted_row) + "\n"
    return formatted_table


def main_loop():
    lab_obj = Lab2App()
    while 1:
        match input(f"1: Обрати файл для Х\n"
                    f"2: Обрати файл для Y\n"
                    f"3: Обрати тип поліному\n"
                    f"4: Обраховувати лямбду через 3 системи: зараз {lab_obj.use_second_lambda_method}\n"
                    f"5: Обраховувати через нормовані значення: зараз {lab_obj.use_normed_values}\n"
                    f"6: Змінити ступінь поліномів, зараз {lab_obj.all_p}\n"
                    f"7: Значення обраховуються для Y{lab_obj.k_y}\n"
                    f"8: Вивести графік (доступно після обрахування значень)\n"
                    f"9: Зберегти у файл\n"
                    f"0: Вихід\n"
                    f"Enter: Обрахувати\n"):
            case '1':
                lab_obj.file_chooser('x')
            case '2':
                lab_obj.file_chooser('y')
            case '3':
                lab_obj.k_pol = int(input("1: поліном Чебишова\n"
                                          "2: поліном Лежандра\n"
                                          "3: поліном Лагера\n"
                                          "4: поліном Ерміта\n"))
            case '4':
                lab_obj.use_second_lambda_method = not lab_obj.use_second_lambda_method
            case '5':
                lab_obj.use_normed_values = not lab_obj.use_normed_values
            case '6':
                k_p = int(input("Введіть порядковий номер Р, який бажаєте змінити (1, 2, 3):\n"))
                val = input(f"Введіть ступінь Р{k_p}:\n")
                lab_obj.change_p(k_p, val)
            case '7':
                lab_obj.k_y = int(input("Введіть допустимий i_Y\n"))
            case '8':
                if not lab_obj.graphic_disabled:
                    lab_obj.do_plot()
                else:
                    print("Спочатку обрахунки\n")
            case '9':
                lab_obj.save_file()
            case '0':
                break
            case '':
                lab_obj.start()
                input("\n\nНатисніть будь-яку кнопку\n\n")
            case _:
                pass


class Lab2App:
    selection = []  # file selection
    use_second_lambda_method = False
    use_normed_values = True
    graphic_disabled = True

    x_table = []
    y_table = []
    normed_x = []   # normed by minmax_scale
    normed_y = []
    n = [[], []]    # dimensions of variables
    all_p = [1, 1, 1]      # powers of polinoms for x1, x2, x3
    k_y = 1         # for what Y we are finding values
    k_pol = 1       # what type of the polinome we are using

    lambdas = []
    psi_table = []
    a_values = []
    f_table = []
    c_values = []
    main_f_table = []
    approximation = 0

    text_out = ""

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
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_table(variable_name, file_path)
        else:
            print("Файл не обрано\n")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_out)
            print(f"File saved at: {file_path}\n")

    def choose_polinome(self, k):
        self.k_pol = k

    def change_p(self, k_p, value):
        if value != '':
            try:
                self.all_p[k_p - 1] = int(value)
            except ValueError:
                print("Це має бути число\n")

    def find_best_p(self):
        approx = []
        for pol_type in range(4):
            pol_approxs = {}
            self.k_pol = pol_type + 1
            for p1 in range(1, 11):
                for p2 in range(1, 11):
                    for p3 in range(1, 11):
                        self.all_p = [p1, p2, p3]
                        self.processing()
                        print(f'APPROXIMATION: {[self.approximation, [p1, p2, p3], self.k_pol]}')
                        pol_approxs[self.approximation] = [[p1, p2, p3], self.k_pol]
            min_approx = min(pol_approxs)
            approx.append([min_approx, pol_approxs[min_approx]])
        return approx

    def structure_lambda(self, l_table=None):
        if type(l_table) is None:
            return [[self.lambdas[j + x_k * p] for p in range(self.all_p[x_k] + 1) for j in range(self.n[0][x_k])]
                    for x_k in range(len(self.n[0]))]
        else:
            return [[l_table[j + x_k * p] for p in range(self.all_p[x_k] + 1) for j in range(self.n[0][x_k])]
                    for x_k in range(len(self.n[0]))]

    def program_values_out(self):
        # normed -> lambdas -> psi -> a -> F(x) -> c -> F(x1, x2, x3)
        # f"approximation = {self.approximation}",
        text_out = [f"Нормовані значення Х:\n{do_first_line('X', self.n[0])}{format_table(self.normed_x)}",
                    f"Нормовані значення Y:\n{do_first_line('Y', self.n[1])}{format_table(self.normed_y)}",
                    f"Лямбди:\n{format_table(self.lambdas)}",
                    f"PSI:\n{do_first_line('PSI', self.n[0])}{format_table(self.psi_table)}",
                    f"PSI через поліном:\n{self.open_psi()}",
                    f"a:\n{format_table(self.a_values)}",
                    f"Ф(xi):\n{do_first_line('Ф', [len(self.n[0])]) + format_table(self.f_table)}",
                    f"Ф(Xi) через поліном:\n{self.open_f()}",
                    f"c:\n{format_table(self.c_values)}",
                    f"Ф{self.k_y}(x1, x2, x3):\n{format_table(self.main_f_table)}",
                    f"Ф{self.k_y}(x1, x2, x3) = {self.open_main_f()}",
                    f"Ф{self.k_y}(x1, x2, x3) через поліном:\n{self.open_pol_main_f()}",
                    f"Ф{self.k_y}(x1, x2, x3) у вигляді багаточлену (у нормованому вигляді):\n{self.open_super_pol_main_f()}",
                    f"Ф{self.k_y}(x1, x2, x3) у вигляді багаточлену (у ненормованому вигляді):\n{self.open_unnormed_super_pol_main_f()}"]
        self.text_out = "\n\n".join(text_out)
        # self.root.ids.tab_normed_x.text = self.text_out
        self.graphic_disabled = False

    def get_values(self, i_y):
        try:
            if 0 < int(i_y) <= len(self.y_table) + 1:
                self.k_y = int(i_y)
        except ValueError:
            pass
        else:
            print("i_y не може бути більшим за\nрозмірність Y")

    def input_table(self, variable_name, file_path):
        print(file_path)
        file = open(file_path, 'r')
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
            print("Таблиці пусті, без даних нічого не спрацює")
        elif len(self.x_table) != len(self.y_table):
            print("А спрацювало б, якби кількість рядків у таблицях співпадала")
        else:
            self.reset_tables()
            self.processing()
            # print(self.find_best_p())

    def processing(self):
        self.x_table = np.array(self.x_table)
        self.y_table = np.array(self.y_table)
        self.normed_x = minmax_scale(self.x_table)
        self.normed_y = minmax_scale(self.y_table)
        # normed -> lambdas -> psi -> a -> F(x) -> c -> F(x1, x2, x3)
        l_table = []
        for x_k in range(len(self.n[0])):
            l_table.extend(self.find_lambda_k_m2(x_k + 1))
        self.lambdas = [self.structure_lambda(self.find_lambdas_m1()), self.structure_lambda(np.array(l_table))][self.use_second_lambda_method]
        print(self.lambdas)
        self.psi_table = self.find_psi()[0]
        self.a_values = self.find_a()
        self.f_table = self.find_f()
        self.c_values = self.find_c()
        self.main_f_table = self.find_main_f()
        self.approximation = self.find_approximation()

        # print(f"\nPolinom:{do_polinom(self.k_pol, self.normed_x[0][0], self.all_p[0])}")
        # print(f"\nlambdas method 1:\n{self.structure_lambda(self.find_lambdas_m1())}")
        # print(f"\nlambdas method 2:\n{self.lambdas}")
        # print(f"\n{self.psi_table}")
        # print(f"\n{self.a_values}")
        # print(f"\nf table{self.f_table}")
        # print(f"\nc val = {self.c_values}")
        # print(f"\nmain F = {self.main_f_table}")
        # print(f"\napproximation = {self.approximation}")
        # print(type(self.f_table))
        # print(do_unnorm(self.f_table))
        self.program_values_out()
        print(self.text_out)

    def do_plot(self):
        fig = plt.figure(figsize=(7, 5), layout='constrained')
        fig_val = fig.subplots(2, 1, sharex=True)

        x_values = np.arange(0, len(self.x_table), 1)
        if self.use_normed_values:
            fig_val[0].plot(x_values, self.main_f_table, label=f"Ф{self.k_y}(x1, x2, x3)")
            fig_val[0].plot(x_values, self.normed_y[:, self.k_y - 1], label=f"normed Y{self.k_y}")
            fig_val[1].plot(x_values,
                            self.find_approximation_values(self.main_f_table, self.normed_y),
                            label=f"approximation")

        else:
            fig_val[0].plot(x_values, do_unnorm(self.main_f_table), label=f"unnormed Ф{self.k_y}(x1, x2, x3)")
            fig_val[0].plot(x_values, self.y_table[:, self.k_y - 1], label=f"real Y{self.k_y}")
            fig_val[1].plot(x_values,
                            self.find_approximation_values(do_unnorm(self.main_f_table), self.y_table),
                            label=f"approximation")
        fig_val[0].set_title(f"max approx = {self.approximation}")
        fig_val[0].grid()
        fig_val[0].legend()
        fig_val[1].grid()
        fig_val[1].legend()
        plt.show()

    def find_lambdas_m1(self):
        all_p = self.all_p
        A = []
        for q in range(len(self.x_table)):
            a_line = []
            # k = 0 1 2
            for k in range(len(self.n[0])):
                pos_x = sum(self.n[0][i] for i in range(k))
                dim_x = self.n[0][k]
                # j = 0 1
                for j in range(dim_x):
                    # p = 0 1 2
                    for p in range(all_p[k] + 1):
                        a_line.append(do_polinom(self.k_pol, self.normed_x[q][j + pos_x], p))
            A.append(a_line)
        A = np.array(A)
        # lambdas for 1st Y (index = k_y)
        return cj.do_conjugate_gradient(A, self.normed_y[:, self.k_y - 1])

    def find_lambda_k_m2(self, k):
        k = k - 1
        print(self.all_p)
        my_p = self.all_p[k]
        dim_x = self.n[0][k]
        A = []
        for q in range(len(self.x_table)):
            a_line = []
            # k = k
            pos_x = sum(self.n[0][i] for i in range(k))
            # j = 0 1
            for j in range(dim_x):
                # p = 0 1 2
                for p in range(my_p + 1):
                    a_line.append(do_polinom(self.k_pol, self.normed_x[q][j + pos_x], p))
            A.append(a_line)
        A = np.array(A)
        lambda_k = cj.do_conjugate_gradient(A, self.normed_y[:, self.k_y - 1])
        return lambda_k

    def open_psi(self):
        text_out = ""
        for x_k in range(len(self.n[0])):
            text_line = []
            my_p = self.all_p[x_k] + 1
            for j in range(self.n[0][x_k]):
                text_sum = ""
                for p in range(my_p):
                    text_sum += f"{'{:.4f}'.format(self.lambdas[x_k][p + j * my_p])} * T{p}(x{x_k + 1}{j + 1})+"
                text_sum = text_sum.replace('+-', ' - ').replace('+', ' + ')
                text_line.append(f"PSI{x_k + 1}{j + 1} = {text_sum[:-3]}\n")
            text_out += "".join(text_line)
        return text_out

    def find_psi(self):
        # k input = 1 ... k
        dim_x = self.n[0]
        sum_var = []
        # q = 0 ... 39
        for q in range(len(self.normed_x)):
            line = []
            # x_k = 0 1 2
            for x_k in range(len(dim_x)):
                my_p = self.all_p[x_k] + 1
                # j = 0 1
                for j in range(dim_x[x_k]):
                    s_var = 0
                    # p = 0 1 2
                    for p in range(my_p):
                        # we take first raw in normed_x for calculating polinom
                        a = self.lambdas[x_k][p + j * my_p]
                        s_var += a * do_polinom(self.k_pol, self.normed_x[q][x_k + j * dim_x[x_k]], p)
                    line.append(s_var)
            sum_var.append(line)
        return [np.array(sum_var), 0]

    def find_a(self):
        return cj.do_conjugate_gradient(self.psi_table, self.normed_y[:, self.k_y - 1])

    def open_f(self):
        lines = []
        for x_k in range(len(self.n[0])):
            pos_x = sum(self.n[0][i] for i in range(x_k))
            text_sum = ""
            for j in range(self.n[0][x_k]):
                text_sum += f"{'{:.4f}'.format(self.a_values[pos_x + j])} * PSI(x{x_k + 1}{j + 1})+"
            text_sum = text_sum.replace('+-', ' - ').replace('+', ' + ')
            lines.append(f"Ф{x_k + 1} = {text_sum[:-3]}\n")
        return "".join(lines)

    def find_f(self):
        dim_x = self.n[0]
        f_table = []
        for q in range(len(self.psi_table)):
            line = []
            for x_k in range(len(dim_x)):
                pos_x = sum(self.n[0][i] for i in range(x_k))
                line.append(sum(self.a_values[pos_x + j] * self.psi_table[q][pos_x + j] for j in range(dim_x[x_k])))
            f_table.append(line)
        return np.array(f_table)

    def find_c(self):
        return cj.do_conjugate_gradient(self.f_table, self.normed_y[:, self.k_y - 1])

    def open_pol_main_f(self):
        f_val = []
        for x_k in range(len(self.n[0])):
            my_p = self.all_p[x_k] + 1
            pos_x = sum(self.n[0][i] for i in range(x_k))
            for j in range(self.n[0][x_k]):
                for p in range(my_p):
                    multiplier = self.lambdas[x_k][p + j * my_p] * self.a_values[pos_x + j] * self.c_values[x_k]
                    f_val.append(f"{multiplier}*T{p}(x{x_k + 1}{j + 1})")
        return ' + '.join(f_val)

    def open_super_pol_main_f(self):
        f_val = []
        for x_k in range(len(self.n[0])):
            my_p = self.all_p[x_k] + 1
            pos_x = sum(self.n[0][i] for i in range(x_k))
            for j in range(self.n[0][x_k]):
                for p in range(my_p):
                    multiplier = self.lambdas[x_k][p + j * my_p] * self.a_values[pos_x + j] * self.c_values[x_k]
                    f_val.append(str(sp.expand(open_polinom(self.k_pol, f"x{x_k + 1}{j + 1}", p) * multiplier)).replace("**", '^'))
        return ' + '.join(f_val)

    def open_unnormed_super_pol_main_f(self):
        f_val = []
        coef_matrix = do_unnorm(self.do_coefficients_matrix())
        print(coef_matrix)
        for x_k in range(len(self.n[0])):
            my_p = self.all_p[x_k] + 1
            pos_x = sum(self.n[0][i] for i in range(x_k))
            for j in range(self.n[0][x_k]):
                for p in range(my_p):
                    multiplier = coef_matrix[pos_x + j][p]
                    f_val.append(str(sp.expand(open_polinom(self.k_pol, f"x{x_k + 1}{j + 1}", p) * multiplier)).replace("**", '^'))
        return ' + '.join(f_val)

    def open_main_f(self):
        text_sum = ""
        for f_k in range(len(self.f_table[0])):
            text_sum += f"{'{:.4f}'.format(self.c_values[f_k])} * Ф(x{f_k + 1})+"
        text_sum = text_sum.replace('+-', ' - ').replace('+', ' + ')
        return text_sum[:-3] + '\n'

    def find_main_f(self):
        f_table = []
        for q in range(len(self.f_table)):
            f_table.append(sum(self.c_values[f_k] * self.f_table[q][f_k] for f_k in range(len(self.f_table[0]))))
        return np.array(f_table)

    def find_approximation_values(self, main_f_table, y_table):
        return [abs(main_f_table[i] - y_table[:, self.k_y - 1][i]) for i in range(len(y_table))]

    def find_approximation(self):
        if self.use_normed_values:
            return max(self.find_approximation_values(self.main_f_table, self.normed_y))
        else:
            return max(self.find_approximation_values(do_unnorm(self.main_f_table), self.y_table))

    def find_unnormed_f(self):
        table = []
        for q in range(len(self.f_table)):
            line = []
            for j in range(len(self.f_table[0])):
                my_column = self.f_table[:, j]
                line.append(self.f_table[q][j] * (max(my_column) - min(my_column)) + min(my_column))
            table.append(line)
        return np.array(table)

    def do_coefficients_matrix(self):
        coef_mtrx = []
        for x_k in range(len(self.n[0])):
            my_p = self.all_p[x_k] + 1
            pos_x = sum(self.n[0][i] for i in range(x_k))
            for j in range(self.n[0][x_k]):
                line = []
                for p in range(my_p):
                    line.append(self.lambdas[x_k][p + j * my_p] * self.a_values[pos_x + j] * self.c_values[x_k])
                coef_mtrx.append(np.array(line))
        return coef_mtrx


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
            return pol.do_chebish_polinom(x, n)
        case 2:
            return pol.do_lezhandr_polinom(x, n)
        case 3:
            return pol.do_lagerr_polinom(x, n)
        case 4:
            return pol.do_ermit_polinom(x, n)


def open_polinom(k_polinom, var_name, n):
    match k_polinom:
        case 1:
            return pol.do_chebish_polinom_univ(var_name, n)
        case 2:
            return pol.do_lezhandr_polinom_univ(var_name, n)
        case 3:
            return pol.do_lagerr_polinom_univ(var_name, n)
        case 4:
            return pol.do_ermit_polinom_univ(var_name, n)


def do_unnorm(origin_table):
    table = []
    if type(origin_table[0]) is np.ndarray:
        for q in range(len(origin_table)):
            line = []
            for j in range(len(origin_table[q])):
                my_column = origin_table[q]
                line.append(origin_table[q][j] * (max(my_column) - min(my_column)) + min(my_column))
            table.append(line)
    else:
        # if origin_table is not a table, but a list:
        for number in origin_table:
            table.append(number * (max(origin_table) - min(origin_table)) + min(origin_table))
    return table


main_loop()
