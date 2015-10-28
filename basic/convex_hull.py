# coding=utf-8
from copy import copy, deepcopy
from basic.constants import epsilon
from gui.primitives import Point, Line
from metrics import euclidean_sqr

from orient import orient

__author__ = 'Michał Ciołczyk'

COUNTER_CLOCKWISE, CLOCKWISE, COLINEAR = (1, -1, 0)


def graham_convex_hull(points, visualization=False):
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

    def get_vis_step(hull, r):
        first = True
        step = []
        for p in hull:
            if not first:
                step.append(Line.from_points(step[-1], p, 'g'))
            cpy = copy(p)
            step.append(cpy)
            first = False
        if len(step) > 0:
            step.append(Line.from_points(step[-1], r, 'y'))
        cpy = copy(r)
        step.append(cpy)
        return step

    steps = []

    def keep_left(hull, r):
        if visualization:
            steps.append(get_vis_step(hull, r))
        while len(hull) > 1 and orient(hull[-2], hull[-1], r) != COUNTER_CLOCKWISE:
            hull.pop()
            if visualization:
                steps.append(get_vis_step(hull, r))
        hull.append(r)
        return hull

    points = sorted(points, cmp=comparator)
    return reduce(keep_left, points, []), steps


def jarvis_convex_hull(points, visualization=False):
    def min_comp(p, q):
        if (p.x < q.x) or (p.x == q.x and p.y < q.y):
            return p
        else:
            return q

    hull = [reduce(min_comp, points)]

    def get_vis_step(r):
        first = True
        step = []
        for p in hull:
            if not first:
                step.append(Line.from_points(step[-1], p, 'g'))
            cpy = copy(p)
            step.append(cpy)
            first = False
        if len(step) > 0:
            step.append(Line.from_points(step[-1], r, 'y'))
        cpy = copy(r)
        step.append(cpy)
        return step

    def next_point(p):
        def comparator(q, r):
            if visualization:
                steps.append(get_vis_step(r))
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

        if visualization:
            steps.append(get_vis_step(points[-1]))

        return reduce(comparator, points)

    p = hull[0]
    steps = []
    while True:
        q = next_point(p)
        hull.append(q)
        p = hull[-1]
        if p == hull[0]:
            break
    return hull, steps
