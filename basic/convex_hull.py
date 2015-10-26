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
    def min_comp(p, q):
        if (p.x < q.x) or (p.x == q.x and p.y < q.y):
            return p
        else:
            return q

    def next_point(p):
        def comparator(q, r):
            o = orient(p, q, r)
            if o == COLINEAR:
                if euclidean_sqr(p, q) > euclidean_sqr(p, r):
                    return q
                else:
                    return r
            else:
                if o == COUNTER_CLOCKWISE:
                    return q
                else:
                    return r

        return reduce(comparator, points)

    hull = [reduce(min_comp, points)]
    p = hull[0]
    while True:
        q = next_point(p)
        hull.append(q)
        p = hull[-1]
        if p == hull[0]:
            break
    return hull
