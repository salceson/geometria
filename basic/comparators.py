# coding=utf-8
from .constants import epsilon

__author__ = 'Michał Ciołczyk'


def compare_lower_x_first_then_lower_y(a, b):
    return a.x - b.x < -epsilon or (abs(a.x - b.x) <= epsilon and a.y - b.y < -epsilon)
