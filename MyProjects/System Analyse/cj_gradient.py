import numpy as np


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
