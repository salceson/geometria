# coding=utf-8
from copy import deepcopy
import sys
import time

from matplotlib import pyplot as plt

from basic.convex_hull import jarvis_convex_hull, graham_convex_hull
from generate import generate_a, generate_b, generate_c, generate_d
from gui.plots import Plot
from gui.primitives import Line

__author__ = 'Michał Ciołczyk'

if __name__ == '__main__':
    argv = sys.argv

    set = sys.argv[1]
    method = sys.argv[2]

    points = []

    if set == 'a':
        points = generate_a(1000, -100, 100)
    if set == 'b':
        points = generate_b(1000, 0, 0, 10)
    if set == 'c':
        points = generate_c(1000, -10, 10, -10, -10, 10, -10, 10, 10)
    if set == 'd':
        points = generate_d(250, 200, 10, 0, 10, 10, 0, 10)

    vis = Plot(points)
    vis.draw()
    plt.savefig('noanim_' + set + '_' + method + '.png')
    # vis.show()

    plot = Plot(points)

    points_copy = deepcopy(points)
    for point in points_copy:
        point.color = 'r'

    hull = []
    steps = []

    if method == 'g':

        print 'Set:', set, 'Method: Graham'

        time_start = time.time()
        hull, steps = graham_convex_hull(points_copy, False)
        time_end = time.time()

        print (time_end - time_start), 's'

    if method == 'j':

        print 'Set:', set, 'Method: Jarvis'

        time_start = time.time()
        hull, steps = jarvis_convex_hull(points_copy, False)
        time_end = time.time()

        print (time_end - time_start), 's'

    prev_point = hull[-1]
    for point in hull:
        plot.add(Line.from_points(prev_point, point, 'g'))
        prev_point = point
    plot.add_all(hull)
    plot.draw()
    plt.savefig('noanim_hull_' + set + '_' + method + '.png')
    # plot.show()
