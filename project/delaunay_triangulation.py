# coding=utf-8
import numpy as np

from gui.primitives import Point
from basic.constants import epsilon
from search_structures import BruteTriangles
from triangles import *

__author__ = 'Michał Ciołczyk, Michał Janczykowski'


def triangulate(points_list, visualization=None):
    point_max_x = reduce(lambda acc, i: points_list[i] if points_list[i].x > acc.x else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_min_x = reduce(lambda acc, i: points_list[i] if points_list[i].x < acc.x else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_max_y = reduce(lambda acc, i: points_list[i] if points_list[i].y > acc.y else acc,
                         xrange(1, len(points_list)), points_list[0])
    point_min_y = reduce(lambda acc, i: points_list[i] if points_list[i].y < acc.y else acc,
                         xrange(1, len(points_list)), points_list[0])

    M = max(point_max_x.x - point_min_x.x, point_max_y.y - point_min_y.y) / 2.0

    middle_point = Point((point_max_x.x + point_min_x.x) / 2.0, (point_max_y.y + point_min_y.y) / 2.0, 'b')

    p1 = middle_point + Point(3 * M + epsilon, 0, 'b')
    p2 = middle_point + Point(0, 3 * M + epsilon, 'b')
    p3 = middle_point + Point(-3 * M - epsilon, -3 * M - epsilon, 'b')

    search_struct = BruteTriangles([Triangle(
        [Edge(p1, p2), None],
        [Edge(p2, p3), None],
        [Edge(p3, p1), None]
    )])

    np.random.shuffle(points_list)

    for p in points_list:
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
            if nt1:
                nt1.set_neighbor(ne1, t1)
            if nt2:
                nt2.set_neighbor(ne2, t2)
            if nt3:
                nt3.set_neighbor(ne3, t3)
            [search_struct.add(t) for t in [t1, t2, t3]]
            # Legalizing edges
            search_struct.legalize_edge(t1, ne1, nt1)
            search_struct.legalize_edge(t2, ne2, nt2)
            search_struct.legalize_edge(t3, ne3, nt3)
        else:
            [ne1, nt1], [ne2, nt2], [ne3, nt3] = triangle.n1, triangle.n2, triangle.n3
            if p in ne1:
                ne = ne1
                nt = nt1
            elif p in ne2:
                ne = ne2
                nt = nt2
            else:
                ne = ne3
                nt = nt3
            if nt:
                (pr, pi, pj, pk, pl) = (p, ne.p2, ne.p1, triangle.opposite_point(ne), nt.opposite_point(ne))
                search_struct.delete(triangle)
                search_struct.delete(nt)
                e_kj = Edge(pk, pj)
                n_kj = triangle.get_neighbor(e_kj)
                e_ik = Edge(pi, pk)
                n_ik = triangle.get_neighbor(e_ik)
                e_jl = Edge(pj, pl)
                n_jl = nt.get_neighbor(e_jl)
                e_li = Edge(pl, pi)
                n_li = nt.get_neighbor(e_li)
                t_rik = Triangle(
                    [Edge(pr, pi), None],
                    [Edge(pi, pk), n_ik],
                    [Edge(pk, pr), None]
                )
                t_rkj = Triangle(
                    [Edge(pr, pk), t_rik],
                    [Edge(pk, pj), n_kj],
                    [Edge(pj, pr), None]
                )
                t_rjl = Triangle(
                    [Edge(pr, pj), t_rkj],
                    [Edge(pj, pl), n_jl],
                    [Edge(pl, pr), None]
                )
                t_rli = Triangle(
                    [Edge(pr, pl), t_rjl],
                    [Edge(pl, pi), n_li],
                    [Edge(pi, pr), t_rik]
                )
                t_rik.n1[1] = t_rli
                t_rik.n3[1] = t_rkj
                t_rkj.n3[1] = t_rjl
                t_rjl.n3[1] = t_rli
                if n_kj:
                    n_kj.set_neighbor(e_kj, t_rkj)
                if n_jl:
                    n_jl.set_neighbor(e_jl, t_rjl)
                if n_li:
                    n_li.set_neighbor(e_li, t_rli)
                if n_ik:
                    n_ik.set_neighbor(e_ik, t_rik)
                # Add triangles
                search_struct.add(t_rli)
                search_struct.add(t_rjl)
                search_struct.add(t_rkj)
                search_struct.add(t_rik)
                # Legalize edges:
                search_struct.legalize_edge(t_rli, e_li, n_li)
                search_struct.legalize_edge(t_rjl, e_jl, n_jl)
                search_struct.legalize_edge(t_rkj, e_kj, n_kj)
                search_struct.legalize_edge(t_rik, e_ik, n_ik)
            else:
                (pr, pi, pj, pk) = (p, ne.p2, ne.p1, triangle.opposite_point(ne))
                search_struct.delete(triangle)
                e_kj = Edge(pk, pj)
                n_kj = triangle.get_neighbor(e_kj)
                e_ik = Edge(pi, pk)
                n_ik = triangle.get_neighbor(e_ik)
                t_rik = Triangle(
                    [Edge(pr, pi), None],
                    [Edge(pi, pk), n_ik],
                    [Edge(pk, pr), None]
                )
                t_rkj = Triangle(
                    [Edge(pr, pk), t_rik],
                    [Edge(pk, pj), n_kj],
                    [Edge(pj, pr), None]
                )
                t_rik.n3[1] = t_rkj
                if n_kj:
                    n_kj.set_neighbor(e_kj, t_rkj)
                if n_ik:
                    n_ik.set_neighbor(e_ik, t_rik)
                # Add triangles
                search_struct.add(t_rkj)
                search_struct.add(t_rik)
                # Legalize edges:
                search_struct.legalize_edge(t_rkj, e_kj, n_kj)
                search_struct.legalize_edge(t_rik, e_ik, n_ik)
        for t in search_struct.triangles:
            print t
        if visualization:
            visualization.clear_figures()
            visualization.add_all_figures(visualization.points)
            for f in search_struct.triangles:
                visualization.add_figure(f)
            visualization.add_all_figures(search_struct.triangles)
            visualization.update_figures()
            visualization.wait(1)

    # remove additional nodes
    additional_nodes = [p1, p2, p3]
    search_struct.triangles[:] = [t for t in search_struct.triangles if
                                  len([p for p in additional_nodes if p in t.get_points()]) == 0]

    print "\nfinal triangulation:"
    for t in search_struct.triangles:
        print t

    if visualization:
        visualization.clear_figures()
        visualization.add_all_figures(visualization.points)
        for f in search_struct.triangles:
            visualization.add_figure(f)
        visualization.add_all_figures(search_struct.triangles)
        visualization.update_figures()
        visualization.wait(1)

    return search_struct.triangles


if __name__ == "__main__":
    points = [Point(2, 0), Point(0, 0), Point(1, 1), Point(1, 2)]
    triangulate(points)
