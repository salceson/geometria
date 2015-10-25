# coding=utf-8
from copy import deepcopy

from basic.convex_hull import *
from generate import *
from gui.plots import *
from gui.primitives import Line

__author__ = 'Michał Ciołczyk'

# points = generate_a(100, -100, 100)
# points = generate_b(100, 0, 0, 10)
points = generate_c(100, -10, 10, -10, -10, 10, -10, 10, 10)


plot = Plot()
plot.add_all(points)
plot.step()
points_copy = deepcopy(points)
for point in points_copy:
    point.color = 'r'
# hull = graham_convex_hull(points_copy)
hull = jarvis_convex_hull(points_copy)
prev_point = hull[-1]
for point in hull:
    plot.add(Line.from_points(prev_point, point, 'g'))
    prev_point = point
plot.add_all(hull)
plot.step()
plot.draw()
plot.show()

