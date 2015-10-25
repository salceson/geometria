# coding=utf-8

import numpy as np

__author__ = 'Michał Ciołczyk'


def euclidean(p1, p2):
    return np.sqrt(euclidean_sqr(p1, p2))


def euclidean_sqr(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def euclidean_vec(vec):
    return np.sqrt(vec[0] ** 2 + vec[1] ** 2)


def euclidean_vecs(vec1, vec2):
    return euclidean_vec([vec2[0] - vec1[0], vec2[1] - vec1[1]])
