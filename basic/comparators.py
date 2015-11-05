# coding=utf-8
from .constants import epsilon

__author__ = 'Michał Ciołczyk'


def compare_lower_x_first_then_lower_y(a, b):
    return a.x - b.x < -epsilon or (abs(a.x - b.x) <= epsilon and a.y - b.y < -epsilon)


def below_y(a, b):
    return a.y < b.y


def above_y(a, b):
    return a.y > b.y


def is_below_or_same_y(a, b):
    return a.y <= b.y


def higher_y_then_lower_x_annotated(a_p1, a_p2):
    a = a_p1[0]
    b = a_p2[0]
    if a.y > b.y or (a.y == b.y and a.x < b.x):
        return -1
    else:
        return 1
