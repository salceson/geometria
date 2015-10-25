# coding=utf-8

from sklearn.neighbors import DistanceMetric

__author__ = 'Michał Ciołczyk'

euclidean_metric = DistanceMetric.get_metric('euclidean')


def euclidean(p1, p2):
    return euclidean_metric.pairwise([[p1.x, p1.y]], [[p2.x, p2.y]])[0][0]


def euclidean_vec(vec):
    return euclidean_metric.pairwise([[0, 0]], [[vec[0], vec[1]]])[0][0]


def euclidean_vecs(vec1, vec2):
    return euclidean_vec([vec2[0] - vec1[0], vec2[1] - vec1[1]])
