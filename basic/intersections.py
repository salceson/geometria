# coding=utf-8
from .det import det

__author__ = 'Michał Ciołczyk'


def _is_in_range(low, high, x):
    return low <= x <= high


def _is_between(a, b, x):
    is_between_x = _is_in_range(a.x, b.x, x.x) or _is_in_range(b.x, a.x, x.x)
    is_between_y = _is_in_range(a.y, b.y, x.y) or _is_in_range(b.y, a.y, x.y)
    return is_between_x and is_between_y


def intersects(segment1, segment2):
    p = segment1.point1
    q = segment2.point1
    r = segment1.point2 - segment1.point1
    s = segment2.point2 - segment2.point1
    det_rs = det(r, s)

    if det_rs == 0.0:
        if det(q - p, r) == 0.0:
            return _is_between(
                segment1.point1, segment1.point2, segment2.point1
            ) or _is_between(
                segment1.point1, segment1.point2, segment2.point2
            )
        else:
            return False
    else:
        t = det(q - p, s) / det_rs
        u = det(q - p, r) / det_rs
        return _is_in_range(0, 1, t) and _is_in_range(0, 1, u)


def get_intersection_point(segment1, segment2):
    p = segment1.point1
    q = segment2.point1
    r = segment1.point2 - segment1.point1
    s = segment2.point2 - segment2.point1
    det_rs = det(r, s)
    t = det(q - p, s) / det_rs
    return p + t * r
