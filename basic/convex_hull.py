# coding=utf-8
from basic.constants import epsilon
from gui.primitives import Point
from metrics import euclidean_sqr

from orient import orient

__author__ = 'Michał Ciołczyk'

COUNTER_CLOCKWISE, CLOCKWISE, COLINEAR = (1, -1, 0)


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
            dist = euclidean_sqr(lowest_Y, p1) - euclidean_sqr(lowest_Y, p2)
            if abs(dist) <= epsilon:
                return 0
            elif dist > epsilon:
                return 1
            else:
                return -1
        else:
            return -orientation

    def keep_left(hull, r):
        while len(hull) > 1 and orient(hull[-2], hull[-1], r) != COUNTER_CLOCKWISE:
            hull.pop()
        hull.append(r)
        return hull

    points = sorted(points, cmp=comparator)
    return reduce(keep_left, points, [])


def jarvis_convex_hull(points, visualization=None):
    def next_point(p):
        q = p
        for r in points:
            orientation = orient(p, q, r)
            if orientation == COUNTER_CLOCKWISE or \
                    (orientation == COLINEAR and euclidean_sqr(p, r) > euclidean_sqr(p, q)):
                q = r
        return q

    hull = [min(points, key=lambda x: x.x)]
    for p in hull:
        q = next_point(p)
        if q != hull[0]:
            hull.append(q)
    return hull
