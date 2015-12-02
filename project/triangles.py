# coding=utf-8

from basic.mixins import OperatorMixin
from basic.orient import orient
from gui.primitives import Polygon

__author__ = 'Michał Ciołczyk, Michał Janczykowski'


def edge_of_neighbor(neighbor):
    return neighbor[0]


def triangle_of_neighbor(neighbor):
    return neighbor[1]


class Triangle(object):
    def __init__(self, n1, n2, n3, color='k'):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.node = None
        self.color = color

    def _point_orient(self, point):
        e1 = edge_of_neighbor(self.n1)
        e2 = edge_of_neighbor(self.n2)
        p1 = e1.p1
        p2 = e1.p2
        p3 = e2.p2
        orient1 = orient(p1, p2, point)
        orient2 = orient(p2, p3, point)
        orient3 = orient(p3, p1, point)
        return orient1 + orient2 + orient3

    def __contains__(self, point):
        return self._point_orient(point) in [2, 3]

    def is_inside(self, point):
        return self._point_orient(point) == 3

    def set_neighbor(self, edge, new_neighbor):
        if edge == edge_of_neighbor(self.n1):
            self.n1[1] = new_neighbor
        if edge == edge_of_neighbor(self.n2):
            self.n2[1] = new_neighbor
        if edge == edge_of_neighbor(self.n3):
            self.n3[1] = new_neighbor

    def opposite_point(self, edge):
        n = None
        if edge == edge_of_neighbor(self.n1):
            n = self.n2
        if edge == edge_of_neighbor(self.n2):
            n = self.n3
        if edge == edge_of_neighbor(self.n3):
            n = self.n1
        return edge_of_neighbor(n).p2

    def get_neighbor(self, e):
        if edge_of_neighbor(self.n1) == e:
            return triangle_of_neighbor(self.n1)
        if edge_of_neighbor(self.n2) == e:
            return triangle_of_neighbor(self.n2)
        if edge_of_neighbor(self.n3) == e:
            return triangle_of_neighbor(self.n3)
        return None

    def get_points(self):
        return [self.n1[0].p1, self.n2[0].p1, self.n3[0].p1]

    def __str__(self):
        return "triangle: (" + str(edge_of_neighbor(self.n1).p1) + ", " + str(
            edge_of_neighbor(self.n2).p1) + ", " + str(edge_of_neighbor(self.n3).p1) + ")"

    def to_polygon(self):
        return Polygon(self.get_points(), self.color)

    def draw(self, ax, d):
        self.to_polygon().draw(ax, d, False)

    def min_x(self):
        points = self.get_points()
        return reduce(lambda acc, x: x.x if x.x < acc else acc, points[1:], points[0].x)

    def min_y(self):
        points = self.get_points()
        return reduce(lambda acc, x: x.y if x.y < acc else acc, points[1:], points[0].y)

    def max_x(self):
        points = self.get_points()
        return reduce(lambda acc, x: x.x if x.x > acc else acc, points[1:], points[0].x)

    def max_y(self):
        points = self.get_points()
        return reduce(lambda acc, x: x.y if x.y > acc else acc, points[1:], points[0].y)


class Edge(OperatorMixin):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return (self.p1 == other.p1 and self.p2 == other.p2) or (self.p1 == other.p2 and self.p2 == other.p1)

    def __lt__(self, other):
        raise NotImplementedError()

    def __str__(self):
        return "edge: (" + str(self.p1) + ", " + str(self.p2) + ")"

    def __contains__(self, point):
        return orient(self.p1, self.p2, point) == 0
