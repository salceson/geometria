# coding=utf-8
import matplotlib.pyplot as plt

try:
    from basic.constants import epsilon
except ImportError:
    epsilon = 1e-13

__author__ = 'Michał Ciołczyk'


# noinspection PyTypeChecker
class Line(object):
    def __init__(self, x1, y1, x2, y2, color, label=None):
        """Creates a line segment from (x1, y1) to (x2, y2) of color `color` and label `label`.

        :param x1: the x coordinate of the first point
        :type x1: float
        :param y1: the y coordinate of the first point
        :type y1: float
        :param x2: the x coordinate of the second point
        :type x2: float
        :param y2: the y coordinate of the second point
        :type y2: float
        :param color: line color (expressed as `matplotlib`'s color)
        :type color: str
        :param label: line label
        :type label: str
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.label = label
        self.point1 = Point(x1, y1, color)
        self.point2 = Point(x2, y2, color)

    @classmethod
    def from_points(cls, p1, p2, color, label=None):
        """Creates a line segment from p1 to p2 of color `color` and label `label`.

        :param p1: first point
        :type p1: Point
        :param p2: second point
        :type p2: Point
        :param color: line color (expressed as `matplotlib`'s color)
        :type color: str
        :param label: line label
        :type label: str
        :return: Line instance.
        :rtype: Line
        """
        return cls(p1.x, p1.y, p2.x, p2.y, color, label)

    def draw(self, ax, dy=0, animate=False):
        if animate:
            figures = [plt.Line2D([self.x1, self.x2], [self.y1, self.y2], color=self.color)]
            x_middle = (self.x1 + self.x2) / 2.0
            y_middle = (self.y1 + self.y2) / 2.0 - dy
            if self.label:
                figures.append(plt.Text(x_middle, y_middle, self.label,
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        fontsize=10))
            return figures
        else:
            ax.plot([self.x1, self.x2], [self.y1, self.y2], c=self.color)
            if self.label:
                x_middle = (self.x1 + self.x2) / 2.0
                y_middle = (self.y1 + self.y2) / 2.0 - dy
                ax.text(x_middle, y_middle, self.label, horizontalalignment='center', verticalalignment='center',
                        fontsize=10)

    def max_y(self):
        return max(self.y1, self.y2)

    def min_y(self):
        return min(self.y1, self.y2)

    def max_x(self):
        return max(self.x1, self.x2)

    def min_x(self):
        return min(self.x1, self.x2)

    def __hash__(self):
        return hash(self.point1) + 31 * hash(self.point2)

    def __eq__(self, other):
        if isinstance(other, Line):
            return self.point1 == other.point1 and self.point2 == other.point2
        else:
            return False

    def to_csv_line(self):
        x1 = "%.20f" % self.x1
        x2 = "%.20f" % self.x2
        y1 = "%.20f" % self.y1
        y2 = "%.20f" % self.y2
        label = ", %s" % self.label if self.label else ''
        return "Line, %s, %s, %s, %s, %s%s" % (x1, y1, x2, y2, self.color, label)


# noinspection PyTypeChecker
class Point(object):
    def __init__(self, x, y, color, label=None):
        self.x = x
        self.y = y
        self.color = color
        self.label = label

    def draw(self, ax, dy=0, animate=False):
        if animate:
            figures = [plt.Line2D([self.x], [self.y], marker='o', color=self.color)]
            if self.label:
                figures.append(plt.Text(self.x, self.y - dy, self.label, horizontalalignment='center',
                                        verticalalignment='center', fontsize=10))

            return figures
        else:
            ax.plot([self.x], [self.y], 'o', c=self.color)
            if self.label:
                ax.text(self.x, self.y - dy, self.label, horizontalalignment='center', verticalalignment='center',
                        fontsize=10)

    def max_y(self):
        return self.y

    def min_y(self):
        return self.y

    def max_x(self):
        return self.x

    def min_x(self):
        return self.x

    def __str__(self):
        return "Point(%f, %f, color=%s)" % (self.x, self.y, self.color)

    def __unicode__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Point):
            return abs(self.x - other.x) <= epsilon and abs(self.y - other.y) <= epsilon and self.color == other.color
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.x) + 31 * hash(self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.color, self.label)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.color, self.label)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(other * self.x, other * self.y, self.color, self.label)
        else:
            raise NotImplementedError("Unsupported type of operand %s" % type(other))

    def __rmul__(self, other):
        return self * other

    def to_csv_line(self):
        x = "%.20f" % self.x
        y = "%.20f" % self.y
        label = ", %s" % self.label if self.label else ''
        return "Point, %s, %s, %s%s" % (x, y, self.color, label)
