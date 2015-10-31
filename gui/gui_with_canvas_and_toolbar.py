# coding=utf-8
import gtk

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

__author__ = 'Michał Ciołczyk'


class GuiWithCanvasAndToolbar(gtk.Window):
    def __init__(self, toolBoxWidgets=[], title="GTK Gui Plot", *args, **kwargs):
        super(GuiWithCanvasAndToolbar, self).__init__(*args, **kwargs)
        self.connect("destroy", lambda x: gtk.main_quit())
        self.set_default_size(1100, 600)
        self.set_title(title)

        table = gtk.Table(1, 2, False)

        self.figures = []
        self.y_max = float("-inf")
        self.x_max = float("-inf")
        self.y_min = float("inf")
        self.x_min = float("inf")
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        canvas = FigureCanvas(self.fig)
        canvas.set_size_request(800, 600)

        table.attach(canvas, 0, 1, 0, 1)

        toolbox = gtk.Table(len(toolBoxWidgets) + 1, 1, False)
        i = 0
        for widget in toolBoxWidgets:
            toolbox.attach(widget, 0, 1, i, i + 1)
            i += 1

        label = gtk.Label("SimGUI")
        toolbox.attach(label, 0, 1, i, i + 1)

        table.attach(toolbox, 1, 2, 0, 1)

        self.canvas = canvas

        self.add(table)

    def add_figure(self, figure):
        self.figures.append(figure)
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

    def add_all_figures(self, figures):
        for f in figures:
            self.add_figure(f)

    def remove_figure(self, figure):
        self.figures.remove(figure)
        self.y_max = float("-inf")
        self.x_max = float("-inf")
        self.y_min = float("inf")
        self.x_min = float("inf")
        for f in self.figures:
            f_y_max = f.max_y()
            f_y_min = f.min_y()
            f_x_max = f.max_x()
            f_x_min = f.min_x()
            if self.x_max < f_x_max:
                self.x_max = f_x_max
            if self.x_min > f_x_min:
                self.x_min = f_x_min
            if self.y_max < f_y_max:
                self.y_max = f_y_max
            if self.y_min > f_y_min:
                self.y_min = f_y_min
        self.update_figures()

    def clear_figures(self):
        self.figures = []
        self.y_max = float("-inf")
        self.x_max = float("-inf")
        self.y_min = float("inf")
        self.x_min = float("inf")
        self.update_figures()

    def update_figures(self, clear=True):
        if clear:
            self.ax.clear()
        if len(self.figures) > 0:
            dx = self.x_max - self.x_min
            dy = self.y_max - self.y_min
            dx *= 0.1
            dy *= 0.1
            self.ax.axis([self.x_min - dx, self.x_max + dx, self.y_min - dy, self.y_max + dy])
            for f in self.figures:
                f.draw(self.ax, (self.y_max - self.y_min) / 20.0)
        self.canvas.draw()

    def main(self):
        self.update_figures(False)
        self.show_all()
        gtk.main()
