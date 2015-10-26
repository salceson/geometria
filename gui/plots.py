# coding=utf-8

import itertools

from matplotlib import pyplot as plt
import matplotlib.animation as animation

__author__ = 'Michał Ciołczyk'


class Plot(object):
    def __init__(self, fig=plt.gcf(), ax=plt.gca()):
        """Creates a new simple plot.

        :param fig: pyplot's figure
        :param ax: pyplot's axes
        """
        self.animated = False
        self.fig = fig
        self.ax = ax
        self.to_draw = []
        self.steps = []
        self.y_min = float('inf')
        self.y_max = float('-inf')
        self.x_min = float('inf')
        self.x_max = float('-inf')

    def add_all(self, figures):
        """Adds all figures into a step (if animated) or into the things to draw.

        :param figures: figures to add
        """
        for figure in figures:
            self.add(figure)

    def add(self, figure):
        """Adds a new figure into a step (if animated) or into the things to draw.

        :param figure: figure to add
        """
        self.to_draw.append(figure)
        f_y_max = figure.max_y()
        f_y_min = figure.min_y()
        f_x_max = figure.max_x()
        f_x_min = figure.min_x()
        if self.x_max < f_x_max:
            self.x_max = f_x_max
        if self.x_min > f_x_min:
            self.x_min = f_x_min
        if self.y_max < f_y_max:
            self.y_max = f_y_max
        if self.y_min > f_y_min:
            self.y_min = f_y_min

    def step(self):
        """Closes the current animation step."""
        if self.animated:
            self.steps.append(self.to_draw)
            self.to_draw = []

    def draw(self):
        """Draws the plot.

        IMPORTANT! If plot is animated, keep reference to return value.
        (See http://stackoverflow.com/questions/21099121/python-matplotlib-unable-to-call-funcanimation-from-inside-a-function)


        :return: animation if animated
        """
        if not self.animated:
            for f in self.to_draw:
                f.draw(self.ax, (self.y_max - self.y_min) / 20.0)
        else:
            def op(lf):
                return list(itertools.chain(*map(lambda f: f.draw(self.ax, (self.y_max - self.y_min) / 20.0, True), lf)))

            drawings = map(op, self.steps)
            all_drawings = list(itertools.chain(*drawings))

            def init():
                [f.set_visible(False) for f in all_drawings]
                [self.ax.add_artist(f) for f in all_drawings]
                return all_drawings

            def step(i):
                if i == len(self.steps):
                    [f.set_visible(False) for f in all_drawings]
                else:
                    if i > 0:
                        [f.set_visible(False) for f in drawings[i - 1]]
                    [f.set_visible(True) for f in drawings[i]]
                return all_drawings

            return animation.FuncAnimation(self.fig, step, len(self.steps) + 1, init, blit=True, interval=1000)

    def show(self):
        """Shows the plot (so no pyplot imports are needed)."""
        dx = self.x_max - self.x_min
        dy = self.y_max - self.y_min
        dx *= 0.1
        dy *= 0.1
        plt.axis([self.x_min - dx, self.x_max + dx, self.y_min - dy, self.y_max + dy])
        plt.show()


class AnimatedPlot(Plot):
    def __init__(self, fig=plt.gcf(), ax=plt.gca()):
        """Creates a new animated plot

        :param fig: pyplot's figure
        :param ax: pyplot's axes
        """
        super(AnimatedPlot, self).__init__(fig, ax)
        self.animated = True
