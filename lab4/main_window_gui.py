# coding=utf-8
import gtk
import os
import time

from basic.triangulation import is_y_monotonic
from gui.file_utils import load_from_file, save_to_file
from gui.primitives import Line, Point, Polygon
from gui.gui_with_canvas_and_toolbar import GuiWithCanvasAndToolbar
from lab4.is_monotonic_gui import IsMonotonicGUI

__author__ = 'Michał Ciołczyk'


# noinspection PyBroadException,PyPep8Naming
class MainWindowGui(GuiWithCanvasAndToolbar):
    def __init__(self, *args, **kwargs):
        infoLabel = gtk.Label("Draw a polygon by pressing\nleft mouse button to enter\n"
                              "the polygon's points. When\nfinished, press right mouse button.")
        clearButton = gtk.Button("Clear")
        clearButton.connect("clicked", self.clearClicked)
        animatedCheckBox = gtk.CheckButton("Animated")
        animatedCheckBox.connect("clicked", self.animatedClicked)
        self.animated = False
        monotonicButton = gtk.Button("Check if polygon is y-monotonic")
        monotonicButton.connect("clicked", self.monotonicClicked)
        algoButton = gtk.Button("Triangulate (y-monotonic polygons only)")
        algoButton.connect("clicked", self.algoClicked)
        openButton = gtk.Button("Load polygon from file...")
        openButton.connect("clicked", self.openButtonClicked)
        saveButton = gtk.Button("Save polygon to file...")
        saveButton.connect("clicked", self.saveButtonClicked)

        toolBox = [infoLabel, clearButton, openButton, saveButton, monotonicButton, animatedCheckBox, algoButton]

        super(MainWindowGui, self).__init__(toolBox, "Lab 4 - monotonic polygon triangulation", *args, **kwargs)

        self.prev_point = None
        self.polygon = None
        self.points = []

    def clearClicked(self, widget, data=None):
        self.clear_figures()
        self.prev_point = None
        self.polygon = None
        self.points = []

    def algoClicked(self, widget, data=None):
        pass

    def openButtonClicked(self, widget, data=None):
        self.clearClicked(None)
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Load polygon from CSV...", action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons=(
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_current_folder(path)
        csvFilter = gtk.FileFilter()
        csvFilter.set_name("CSV Files")
        csvFilter.add_pattern("*.csv")
        chooser.add_filter(csvFilter)
        allFilter = gtk.FileFilter()
        allFilter.set_name("All files")
        allFilter.add_pattern("*.*")
        chooser.add_filter(allFilter)
        try:
            response = chooser.run()
            if response == gtk.RESPONSE_OK:
                figures = load_from_file(chooser.get_filename())
                for f in figures:
                    if isinstance(f, Polygon):
                        self.add_figure(f)
                        self.polygon = f
                        break
            has_polygon = True if self.polygon else False
            self.update_figures(polygon=has_polygon)
        finally:
            chooser.destroy()

    def saveButtonClicked(self, widget, data=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Save polygon to CSV...", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        chooser.set_current_folder(path)
        chooser.set_current_name("polygon.csv")
        csvFilter = gtk.FileFilter()
        csvFilter.set_name("CSV Files")
        csvFilter.add_pattern("*.csv")
        chooser.add_filter(csvFilter)
        allFilter = gtk.FileFilter()
        allFilter.set_name("All files")
        allFilter.add_pattern("*.*")
        chooser.add_filter(allFilter)
        try:
            response = chooser.run()
            if response == gtk.RESPONSE_OK:
                save_to_file(chooser.get_filename(), [self.polygon])
        finally:
            chooser.destroy()

    def animatedClicked(self, widget, data=None):
        self.animated = not self.animated

    def handle_click(self, event):
        button = event.button
        if button == 1:
            new_point = Point(event.xdata, event.ydata, 'r')
            prev_point = self.prev_point
            if prev_point:
                line = Line.from_points(prev_point, new_point, 'r')
                self.add_figure(line)
            else:
                self.points = []
                self.polygon = None
                self.clear_figures(False)
            self.add_figure(new_point)
            self.prev_point = new_point
            self.points.append(new_point)
            self.update_figures()
            self.wait(0.05)
        elif button == 3 and len(self.points) >= 3:
            self.clear_figures(False)
            self.polygon = Polygon(self.points, 'r')
            self.add_figure(self.polygon)
            self.update_figures(polygon=True)
            self.prev_point = None
            self.wait(0.05)

    def monotonicClicked(self, widget, data=None):
        if self.polygon:
            time_start = time.time()
            result = is_y_monotonic(self.polygon)
            time_end = time.time()
            IsMonotonicGUI(result, time_end - time_start)
