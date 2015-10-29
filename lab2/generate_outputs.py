# coding=utf-8
from copy import deepcopy
import sys
import time

from basic.convex_hull import jarvis_convex_hull, graham_convex_hull
from generate import generate_a, generate_b, generate_c, generate_d
from gui.plots import AnimatedPlot, Plot
from gui.primitives import Line
from matplotlib import pyplot as plt

__author__ = 'Michał Ciołczyk'

if __name__ == '__main__':
    argv = sys.argv

    set = sys.argv[1]
    method = sys.argv[2]

    show = len(sys.argv) > 3

    points = []

    if set == 'a':
        points = generate_a(100, -100, 100)
    if set == 'b':
        points = generate_b(100, 0, 0, 10)
    if set == 'c':
        points = generate_c(100, -10, 10, -10, -10, 10, -10, 10, 10)
    if set == 'd':
        points = generate_d(25, 20, 10, 0, 10, 10, 0, 10)

    vis = Plot(points)
    vis.draw()
    plt.savefig(set + '_' + method + '.png')

    plot = AnimatedPlot(points)
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

        hull, steps = graham_convex_hull(points_copy, True)
    if method == 'j':

        print 'Set:', set, 'Method: Jarvis'

        time_start = time.time()
        hull, steps = jarvis_convex_hull(points_copy, False)
        time_end = time.time()

        print (time_end - time_start), 's'

        hull, steps = jarvis_convex_hull(points_copy, True)

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

    if show:
        plot.show()
    else:
        anim.save('visualization_' + set + '_' + method + '.mp4', extra_args=['-vcodec', 'libx264'])
        # anim.save('visualization.gif', writer='imagemagick')
