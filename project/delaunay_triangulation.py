# coding=utf-8
import numpy as np

from basic.mixins import OperatorMixin
from basic.orient import orient
from gui.primitives import Point

__author__ = 'Michał Ciołczyk, Michał Janczykowski'


def edge_of_neighbor(neighbor):
    return neighbor[0]


def triangle_of_neighbor(neighbor):
    return neighbor[1]


class Triangle(object):
    def __init__(self, n1, n2, n3):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

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

    def __str__(self):
        return "triangle: (" + str(edge_of_neighbor(self.n1).p1) + ", " + str(edge_of_neighbor(self.n2).p1) + ", " + str(edge_of_neighbor(self.n3).p1) + ")"


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


def is_illegal(t, pk):
    e1 = edge_of_neighbor(t.n1)
    e2 = edge_of_neighbor(t.n2)
    p1 = e1.p1
    p2 = e1.p2
    p3 = e2.p2
    determinant = + (p1.x - pk.x) * (p2.y - pk.y) * (p3.x ** 2 - pk.x ** 2 + p3.y ** 2 - pk.y ** 2) \
                  + (p1.y - pk.y) * (p2.x ** 2 - pk.x ** 2 + p2.y ** 2 - pk.y ** 2) * (p3.x - pk.x) \
                  + (p1.x ** 2 - pk.x ** 2 + p1.y ** 2 - pk.y ** 2) * (p2.x - pk.x) * (p3.y - pk.y) \
                  - (p1.x ** 2 - pk.x ** 2 + p1.y ** 2 - pk.y ** 2) * (p2.y - pk.y) * (p3.x - pk.x) \
                  - (p1.y - pk.y) * (p2.x - pk.x) * (p3.x ** 2 - pk.x ** 2 + p3.y ** 2 - pk.y ** 2) \
                  - (p1.x - pk.x) * (p2.x ** 2 - pk.x ** 2 + p2.y ** 2 - pk.y ** 2) * (p3.y - pk.y)
    return determinant > 0


class BruteTriangles(object):
    def __init__(self, triangles):
        self.triangles = triangles

    def find(self, point):
        for triangle in self.triangles:
            if point in triangle:
                return triangle
        return None

    def legalize_edge(self, t1, e, t2):
        """Legalizes edge.

        :param t1: inserted triangle having edge e
        :param e: edge
        :param t2: already existing neighbor having edge e
        """
        if t2 is None:
            # t1 is external, nothing to do
            return

        pk = t2.opposite_point(e)
        pr = t1.opposite_point(e)
        pi = e.p1
        pj = e.p2
        if is_illegal(t1, pk):
            self.delete(t1)
            self.delete(t2)

            # 4 neighbors of t1 and t2:
            n_ri = t1.get_neighbor(Edge(pr, pi))
            n_ik = t2.get_neighbor(Edge(pi, pk))
            n_kj = t2.get_neighbor(Edge(pk, pj))
            n_jr = t1.get_neighbor(Edge(pj, pr))

            new_t1 = Triangle(
                [Edge(pr, pi), n_ri],
                [Edge(pi, pk), n_ik],
                [Edge(pk, pr), None]
            )
            new_t2 = Triangle(
                [Edge(pr, pk), new_t1],
                [Edge(pk, pj), n_kj],
                [Edge(pj, pr), n_jr]
            )
            new_t1.n3[1] = new_t2

            # set 4 neighbors references to new triangles:
            if n_ri is not None:
                n_ri.set_neighbor(Edge(pr, pi), new_t1)
            if n_ik is not None:
                n_ik.set_neighbor(Edge(pi, pk), new_t1)
            if n_kj is not None:
                n_kj.set_neighbor(Edge(pk, pj), new_t2)
            if n_jr is not None:
                n_jr.set_neighbor(Edge(pj, pr), new_t2)

            self.add(new_t1)
            self.add(new_t2)
            self.legalize_edge(new_t1, new_t1.n2[0], new_t1.n2[1])
            self.legalize_edge(new_t2, new_t2.n2[0], new_t2.n2[1])

    def delete(self, triangle):
        n1 = triangle.n1
        n2 = triangle.n2
        n3 = triangle.n3
        t1 = triangle_of_neighbor(n1)
        t2 = triangle_of_neighbor(n2)
        t3 = triangle_of_neighbor(n3)
        if t1 is not None:
            t1.set_neighbor(edge_of_neighbor(n1), None)
        if t2 is not None:
            t2.set_neighbor(edge_of_neighbor(n2), None)
        if t3 is not None:
            t3.set_neighbor(edge_of_neighbor(n3), None)
        self.triangles.remove(triangle)
        return n1, n2, n3

    def add(self, triangle):
        self.triangles.append(triangle)


def triangulate(points_list, visualization=None):
    point_max_x = reduce(lambda acc, i: points_list[i] if points_list[i].x > acc.x else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_min_x = reduce(lambda acc, i: points_list[i] if points_list[i].x < acc.x else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_max_y = reduce(lambda acc, i: points_list[i] if points_list[i].y > acc.y else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_min_y = reduce(lambda acc, i: points_list[i] if points_list[i].y < acc.y else acc,
                         xrange(1, len(points_list)), points_list[0])

    M = max(point_max_x.x - point_min_x.x, point_max_y.y - point_min_y.y)/2.0

    middle_point = Point((point_max_x.x + point_min_x.x) / 2.0, (point_max_y.y + point_min_y.y) / 2.0, 'b')

    p1 = middle_point + Point(3 * M, 0, 'b')
    p2 = middle_point + Point(0, 3 * M, 'b')
    p3 = middle_point + Point(-3 * M, -3 * M, 'b')

    search_struct = BruteTriangles([Triangle(
        [Edge(p1, p2), None],
        [Edge(p2, p3), None],
        [Edge(p3, p1), None]
    )])

    np.random.shuffle(points_list)

    for p in points_list:
        for t in search_struct.triangles:
            print t
        print "\ninserting point: " + str(p)
        triangle = search_struct.find(p)
        if triangle.is_inside(p):
            [ne1, nt1], [ne2, nt2], [ne3, nt3] = search_struct.delete(triangle)
            t1 = Triangle(
                [ne1, nt1],
                [Edge(ne1.p2, p), None],
                [Edge(p, ne1.p1), None]
            )
            t2 = Triangle(
                [ne2, nt2],
                [Edge(ne2.p2, p), None],
                [Edge(p, ne2.p1), t1]
            )
            t3 = Triangle(
                [ne3, nt3],
                [Edge(ne3.p2, p), t1],
                [Edge(p, ne3.p1), t2]
            )
            t2.n2[1] = t3
            t1.n2[1] = t2
            t1.n3[1] = t3
            if nt1 is not None:
                nt1.set_neighbor(ne1, t1)
            if nt2 is not None:
                nt2.set_neighbor(ne2, t2)
            if nt3 is not None:
                nt3.set_neighbor(ne3, t3)
            [search_struct.add(t) for t in [t1, t2, t3]]
            # Legalizing edges
            search_struct.legalize_edge(t1, ne1, nt1)
            search_struct.legalize_edge(t2, ne2, nt2)
            search_struct.legalize_edge(t3, ne3, nt3)
        else:
            pass
    pass

if __name__ == "__main__":
    points = [Point(0.1,0.1), Point(2,0), Point(1.1,2), Point(1,1)]
    triangulate(points)