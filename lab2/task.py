# coding=utf-8
from copy import deepcopy

from basic.convex_hull import jarvis_convex_hull, graham_convex_hull
from generate import generate_a, generate_b, generate_c, generate_d
from gui.plots import AnimatedPlot
from gui.primitives import Line
import time

__author__ = 'Michał Ciołczyk'

if __name__ == '__main__':
    points = generate_a(100, -100, 100)
    # points = generate_b(100, 0, 0, 10)
    # points = generate_c(100, -10, 10, -10, -10, 10, -10, 10, 10)
    # points = generate_d(25, 20, 10, 0, 10, 10, 0, 10)

    plot = AnimatedPlot(points)
    points_copy = deepcopy(points)
    for point in points_copy:
        point.color = 'r'
    hull, steps = graham_convex_hull(points_copy, True)
    # hull, steps = jarvis_convex_hull(points_copy)
    for step in steps:
        plot.step()
        plot.add_all(step)
    plot.step()
    for _ in range(10):
        prev_point = hull[-1]
        for point in hull:
            plot.add(Line.from_points(prev_point, point, 'g'))
            prev_point = point
        plot.add_all(hull)
        plot.step()
    anim = plot.draw()
    # anim.save('visualization.mp4')
    plot.show()
