# coding=utf-8
from triangles import *
from gui.primitives import Point

__author__ = 'Michał Ciołczyk, Michał Janczykowski'


class AbstractTriangles(object):
    def __init__(self, triangles):
        self.triangles = triangles

    def find(self, point):
        raise NotImplementedError

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

            self.add(new_t1, t1, t2)
            self.add(new_t2, t1, t2)
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

    def add(self, triangle, parent_tr1, parent_tr2=None):
        self.triangles.append(triangle)


class _Node(object):
    def __init__(self, triangle, children=None):
        if not children:
            children = []
        self.triangle = triangle
        self.children = children

    def find(self, point):
        """
        :type point: Point
        """
        if len(self.children) == 0:
            return self

        for n in self.children:
            if point in n.triangle:
                return n.find(point)

        raise StandardError("No way")

    def add(self, child):
        self.children.append(child)


class KirkPatrickTriangles(AbstractTriangles):
    def __init__(self, triangles):
        super(KirkPatrickTriangles, self).__init__(triangles)
        root_triangle = triangles[0]
        self.root = _Node(root_triangle)
        root_triangle.node = self.root

    def find(self, point):
        node = self.root.find(point)
        return node.triangle

    def add(self, triangle, parent_tr1, parent_tr2=None):
        super(KirkPatrickTriangles, self).add(triangle, parent_tr1, parent_tr2)
        t_node = _Node(triangle)
        triangle.node = t_node

        parent_node1 = parent_tr1.node
        parent_node1.add(t_node)

        if parent_tr2:
            parent_node2 = parent_tr2.node
            parent_node2.add(t_node)


class BruteTriangles(AbstractTriangles):
    def __init__(self, triangles):
        super(BruteTriangles, self).__init__(triangles)

    def find(self, point):
        for triangle in self.triangles:
            if point in triangle:
                return triangle
        return None


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
