# coding=utf-8

__author__ = 'Michał Ciołczyk'


def det(p, q):
    return p.x * q.y - p.y * q.x


def det3(p, q, rel):
    return det(p - rel, q - rel)
