# coding=utf-8
from basic.constants import epsilon
from gui.primitives import Point
from metrics import euclidean

from orient import orient

__author__ = 'Michał Ciołczyk'

COUNTER_CLOCKWISE, CLOCKWISE, COLINEAR = (1, -1, 0)


def _keep_left(hull, r, visualization=None):
    while len(hull) > 1 and orient(hull[-2], hull[-1], r) != COUNTER_CLOCKWISE:
        hull.pop()
    hull.append(r)
    return hull


def graham_convex_hull(points, visualization=None):
    """Returns points on convex hull of an array of points in CCW order."""
    # Find the point with lowest y coordinate (and lowest x coordinate
    # if there are more than one point with lowest y coordinate)
    lowest_Y = Point(float("inf"), float("inf"), 'b')
    for point in points:
        if point.y < lowest_Y.y - epsilon:
            lowest_Y = point
        elif abs(point.y - lowest_Y.y) <= epsilon and point.x < lowest_Y.x:
            lowest_Y = point

    # Comparator used to compare 2 points while sorting by angle
    def comparator(p1, p2):
        orientation = orient(lowest_Y, p1, p2)
        if orientation == COLINEAR:
            dist = euclidean(lowest_Y, p1) - euclidean(lowest_Y, p2)
            if abs(dist) <= epsilon:
                return 0
            elif dist > epsilon:
                return 1
            else:
                return -1
        else:
            return -orientation

    points = sorted(points, cmp=comparator)
    return reduce(lambda hull, r: _keep_left(hull, r, visualization), points, [])


def jarvis_convex_hull(points, visualization=None):
    pass
