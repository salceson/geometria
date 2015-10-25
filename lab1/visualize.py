# coding=utf-8

from matplotlib import pyplot as plt
import sys

__author__ = 'Michał Ciołczyk'

filename_in = sys.argv[1]
split_points = sys.argv[2] == '1'
show = sys.argv[3] == '1'

x_above = []
x_at = []
x_below = []
y_above = []
y_at = []
y_below = []

EPSILON = 1e-14

with open(filename_in) as f:
    for line in f:
        if split_points:
            x, y, det = line.split(' ')
            x = float(x)
            y = float(y)
            det = float(det)
            if det < -EPSILON:
                x_below.append(x)
                y_below.append(y)
            elif det > EPSILON:
                x_above.append(x)
                y_above.append(y)
            else:
                x_at.append(x)
                y_at.append(y)
        else:
            x, y = line.split(' ')
            x = float(x)
            y = float(y)
            x_above.append(x)
            y_above.append(y)

if split_points:
    print 'Points with det > 0 (above line):', len(x_above)
    print 'Points with det = 0 (at line):', len(x_at)
    print 'Points with det < 0 (below line):', len(x_below)
    plt.axes().set_aspect('equal', 'datalim')
    plt.plot(x_below, y_below, 'ob')
    plt.plot(x_above, y_above, 'or')
    plt.plot(x_at, y_at, 'og')
    plt.legend(['Above line (det > 0)', 'Below line (det < 0)', 'At line (det = 0)'])
    filename_out = filename_in[:-3] + 'png' if filename_in[-2:] == 'ut' else filename_in[:-2] + 'png'
    plt.savefig(filename_out)
    if show:
        plt.show()
else:
    plt.axes().set_aspect('equal', 'datalim')
    plt.plot(x_above, y_above, 'or')
    filename_out = filename_in[:-3] + 'png' if filename_in[-2:] == 'ut' else filename_in[:-2] + 'png'
    plt.savefig(filename_out)
    if show:
        plt.show()
