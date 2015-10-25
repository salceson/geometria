# coding=utf-8
from basic.constants import epsilon

__author__ = 'Michał Ciołczyk'


def orient(p, q, r):
    orientation = (q.x - p.x) * (r.y - p.y) - (r.x - p.x) * (q.y - p.y)
    if abs(orientation) <= epsilon:
        return 0
    elif orientation > epsilon:
        return 1
    else:
        return -1
