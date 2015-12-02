# coding=utf-8

import numpy as np

from gui.primitives import Point

__author__ = 'Michał Ciołczyk'


def generate_random(n, x_min, x_max, y_min, y_max):
    xs = np.random.uniform(x_min, x_max, n)
    ys = np.random.uniform(y_min, y_max, n)
    points = []
    for i in xrange(n):
        points.append(Point(xs[i], ys[i]))
    return points
