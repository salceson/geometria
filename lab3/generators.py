# coding=utf-8

import numpy as np

from gui.primitives import Line

__author__ = 'Michał Ciołczyk'


def generate_random(n, x_min, x_max, y_min, y_max, labels=False):
    x1s = np.random.uniform(x_min, x_max, n)
    x2s = np.random.uniform(x_min, x_max, n)
    y1s = np.random.uniform(y_min, y_max, n)
    y2s = np.random.uniform(y_min, y_max, n)
    segments = []
    for i in xrange(n):
        x1 = x1s[i]
        x2 = x2s[i]
        y1 = y1s[i]
        y2 = y2s[i]
        if x2 < x1:
            (x2, x1) = (x1, x2)
            (y2, y1) = (y1, y2)
        segments.append(Line(x1, y1, x2, y2, 'r', 'Line %d' % i if labels else None))
    return segments
