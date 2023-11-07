from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from plyer import filechooser
import numpy as np

'''    def build(self):
        return Builder.load_file("Lab2.kv")'''

x_table = []
y_table = []


class Lab2App(MDApp):
    Config.set("graphics", "fullscreen", 0)     # "auto"
    Config.write()

    # choose X
    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            print(selection)
            self.root.ids.selected_path.text = selection[0]


def processing_x():  # self, selection
    x = "q	X11 X12	X21	X22	X31	X32\n" \
        "1	0	1	0	1	0	0,5\n" \
        "2	0,1	0,9	0,19	0,91	0,18	0,6\n" \
        "3	0,2	0,8	0,29	0,81	0,28	0,7\n" \
        "4	0,3	0,7	0,39	0,71	0,38	0,8\n" \
        "5	0,4	0,6	0,49	0,61	0,48	0,9\n" \
        "6	0,5	0,5	0,59	0,51	0,58	1\n" \
        "7	0,6	0,4	0,69	0,41	0,68	0,4\n" \
        "8	0,7	0,3	0,79	0,31	0,78	0,3\n" \
        "9	0,8	0,2	0,89	0,21	0,88	0,2\n" \
        "10	0,9	0,1	0,99	0,11	0,98	0,1"
    processed_x = []
    c = 0
    # we don't read name raw
    for item in x.split('\n'):
        if item == '' or c == 0:
            c += 1
            pass
        else:
            processed_x.append(item.split('\t'))

    # considering that 1st line is variables` names, and 1 column is its number
    print(processed_x)
    print(do_norm(processed_x))


def do_norm(table):
    # we don't count q column
    for i in range(1, len(table[0])):
        my_column = [float(raw[i].replace(',', '.')) for raw in table]
        min_val = min(my_column)
        max_val = max(my_column)
        print(i, min_val, max_val)
        for k in range(len(table)):
            table[k][i] = float('{:.4f}'.format((float(table[k][i].replace(',', '.')) - min_val) / (max_val - min_val)))
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


# Lab2App().run()
processing_x()
