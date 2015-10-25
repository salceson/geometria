# coding=utf-8
from primitives import *
from plots import *

__author__ = 'Michał Ciołczyk'

line1 = Line(0, 0, 1, 1, 'r', 'test')
point1 = Point(0.2, 0.3, 'b', 'troll')


plot = AnimatedPlot()
plot.add(line1)
plot.step()
plot.add(point1)
plot.step()
ani = plot.draw()
plot.show()
