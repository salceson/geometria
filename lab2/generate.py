# coding=utf-8

import numpy as np
from gui.primitives import Point
from basic.metrics import euclidean_vec

__author__ = 'Michał Ciołczyk'


def generate_a(n, min, max):
    xs = np.random.uniform(min, max, n)
    ys = np.random.uniform(min, max, n)
    return [Point(xs[i], ys[i], 'b') for i in xrange(n)]


def generate_b(n, x, y, r):
    phis = np.random.uniform(0, 2 * np.pi, n)
    return [Point(x + r * np.cos(phis[i]), y + r * np.sin(phis[i]), 'b') for i in xrange(n)]


def generate_c(n, x1, y1, x2, y2, x3, y3, x4, y4):
    vec_1 = (x2 - x1, y2 - y1)
    vec_2 = (x3 - x2, y3 - y2)
    vec_3 = (x4 - x3, y4 - y3)
    vec_4 = (x1 - x4, y1 - y4)
    len_1 = euclidean_vec(vec_1)
    len_2 = euclidean_vec(vec_2)
    len_3 = euclidean_vec(vec_3)
    len_4 = euclidean_vec(vec_4)
    prob_1 = len_1 / (len_1 + len_2 + len_3 + len_4)
    prob_2 = len_2 / (len_1 + len_2 + len_3 + len_4)
    prob_3 = len_3 / (len_1 + len_2 + len_3 + len_4)
    points = []
    ts = np.random.uniform(0.0, 1.0, n)
    probs = np.random.uniform(0.0, 1.0, n)
    for i in xrange(n):
        t = ts[i]
        if probs[i] < prob_1:
            points.append(Point(x1 + t * vec_1[0], y1 + t * vec_1[1], 'b'))
        elif probs[i] < prob_1 + prob_2:
            points.append(Point(x2 + t * vec_2[0], y2 + t * vec_2[1], 'b'))
        elif probs[i] < prob_1 + prob_2 + prob_3:
            points.append(Point(x3 + t * vec_3[0], y3 + t * vec_3[1], 'b'))
        else:
            points.append(Point(x4 + t * vec_4[0], y4 + t * vec_4[1], 'b'))
    return points


def generate_d(n1, n2, x2, y2, x3, y3, x4, y4):
    (x1, y1) = (0, 0)
    vec_ax1 = (x2 - x1, y2 - y1)
    vec_ax2 = (x4 - x1, y4 - y1)
    vec_diag1 = (x3 - x1, y3 - y1)
    vec_diag2 = (x4 - x2, y4 - y2)
    points = []
    ts1 = np.random.uniform(0.0, 1.0, 2 * n1)
    ts2 = np.random.uniform(0.0, 1.0, 2 * n2)
    for i in xrange(0, 2 * n1, 2):
        t = ts1[i]
        points.append(Point(x1 + t * vec_ax1[0], y1 + t * vec_ax1[1], 'b'))
        t = ts1[i + 1]
        points.append(Point(x1 + t * vec_ax2[0], y1 + t * vec_ax2[1], 'b'))
    for i in xrange(0, 2 * n2, 2):
        t = ts2[i]
        points.append(Point(x1 + t * vec_diag1[0], y1 + t * vec_diag1[1], 'b'))
        t = ts2[i + 1]
        points.append(Point(x2 + t * vec_diag2[0], y2 + t * vec_diag2[1], 'b'))
    return points
