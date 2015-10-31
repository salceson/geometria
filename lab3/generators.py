# coding=utf-8

import numpy as np

from gui.primitives import Line

__author__ = 'Michał Ciołczyk'


def generate_random(n, x_min, x_max, y_min, y_max, labels=False):
    x1s = np.random.uniform(x_min, x_max, n)
    x2s = np.random.uniform(x_min, x_max, n)
    y1s = np.random.uniform(y_min, y_max, n)
    y2s = np.random.uniform(y_min, y_max, n)
    return [Line(x1s[i], y1s[i], x2s[i], y2s[i], 'r', 'Line %d' % i if labels else None) for i in xrange(n)]
