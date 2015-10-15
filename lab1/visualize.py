# coding=utf-8

from matplotlib import pyplot as plt
import sys

__author__ = 'Michał Ciołczyk'

filename_in = sys.argv[1]
split_points = sys.argv[2] == '1'
show = sys.argv[3] == '1'

x1 = []
x2 = []
x3 = []
y1 = []
y2 = []
y3 = []
points1 = 0
points2 = 0
points3 = 0

with open(filename_in) as f:
    for line in f:
        if split_points:
            x, y, det = line.split(' ')
            x = float(x)
            y = float(y)
            det = float(det)
            if det > 0.0:
                x1.append(x)
                y1.append(y)
                points1 += 1
            elif det == 0.0:
                x2.append(x)
                y2.append(y)
                points2 += 1
            else:
                x3.append(x)
                y3.append(y)
                points3 += 1
        else:
            x, y = line.split(' ')
            x = float(x)
            y = float(y)
            x1.append(x)
            y1.append(y)

if split_points:
    print 'Points with det > 0 (above line):', points1
    print 'Points with det = 0 (at line):', points2
    print 'Points with det < 0 (below line):', points3
    plt.plot(x1, y1, 'or')
    plt.plot(x2, y2, 'og')
    plt.plot(x3, y3, 'ob')
    plt.legend(['>0', '=0', '<0'])
    filename_out = filename_in[:-3] + 'png' if filename_in[-2:] == 'ut' else filename_in[:-2] + 'png'
    plt.savefig(filename_out)
    if show:
        plt.show()
else:
    plt.plot(x1, y1, 'or')
    filename_out = filename_in[:-3] + 'png' if filename_in[-2:] == 'ut' else filename_in[:-2] + 'png'
    plt.savefig(filename_out)
    if show:
        plt.show()
