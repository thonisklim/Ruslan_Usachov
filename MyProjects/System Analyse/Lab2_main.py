from kivy import Config
from kivymd.app import MDApp
from plyer import filechooser
import numpy as np

Config.set("graphics", "fullscreen", 0)     # "auto"
Config.write()


class Lab2App(MDApp):
    x_table = []
    y_table = []
    selection = []

    # choose X
    def file_chooser(self, variable_name):
        filechooser.open_file(on_selection=self.get_path)
        self.input_table(variable_name)

    def get_path(self, selection):
        self.selection = selection

    def input_table(self, variable_name):
        if self.selection:
            print(self.selection)
            file = open(self.selection[0], 'r')
            skip = 1
            for line in file.read().split('\n'):
                if line == '' or skip:
                    # we're skipping name raw, or empty raw
                    skip = 0
                else:
                    match variable_name:
                        case 'x':
                            self.x_table.append(line.replace(',', '.').split('\t'))
                        case 'y':
                            self.y_table.append(line.replace(',', '.').split('\t'))
                        case _:
                            exit("wrong variable_name")
                            break
            # self.root.ids.selected_path.text = selection[0]
            # print(self.x_table)

    def start(self):
        if self.x_table == [] or self.y_table == []:
            print("Will You consider filling tables up?")
        else:
            self.processing()

    def processing(self):  # self, selection
        x = self.x_table
        y = self.y_table
        # considering that 1st line is variables` names, and 1 column is its number
        print('\n')
        print(do_norm(x))
        b_q = do_norm(y)
        print('\n')
        print(b_q)


def do_norm(table):
    # we don't normalise q column
    for i in range(1, len(table[0])):
        my_column = [float(raw[i]) for raw in table]
        min_val = min(my_column)
        max_val = max(my_column)
        # print(i, min_val, max_val, my_column)
        for k in range(len(table)):
            table[k][i] = float('{:.4f}'.format((float(table[k][i]) - min_val) / (max_val - min_val)))
    return table


def conjugate_gradient(A, b, x=None, tol=1e-10, max_iter=None):
    n = len(b)
    if x is None:
        x = np.zeros(n)
    r = b - np.dot(A, x)
    p = r
    rsold = np.dot(r, r)
    for i in range(n):
        Ap = np.dot(A, p)
        alpha = rsold / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rsnew = np.dot(r, r)
        if np.sqrt(rsnew) < tol:
            break
        p = r + (rsnew / rsold) * p
        rsold = rsnew
        if max_iter is not None and i >= max_iter:
            break
    return x


Lab2App().run()
