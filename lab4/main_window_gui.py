# coding=utf-8
import gtk
import os
import time

from basic.shamos_hoey_sweep import shamos_hoey_intersections
from gui.file_utils import load_from_file, save_to_file
from gui.primitives import Line, Point
from gui.gui_with_canvas_and_toolbar import GuiWithCanvasAndToolbar
from lab3.algorithm_results import AlgorithmResultsGUI
from lab3.generate_gui import GenerateGui

__author__ = 'Michał Ciołczyk'


# noinspection PyBroadException,PyPep8Naming
class MainWindowGui(GuiWithCanvasAndToolbar):
    def __init__(self, *args, **kwargs):
        generateButton = gtk.Button("Generate data...")
        generateButton.connect("clicked", self.generateClicked)
        clearButton = gtk.Button("Clear")
        clearButton.connect("clicked", self.clearClicked)
        self.animatedCheckBox = gtk.CheckButton("Animated")
        self.animatedCheckBox.connect("clicked", self.animatedClicked)
        self.animated = False
        algoButton = gtk.Button("Run algorithm")
        algoButton.connect("clicked", self.algoClicked)
        openButton = gtk.Button("Load segments from file...")
        openButton.connect("clicked", self.openButtonClicked)
        saveButton = gtk.Button("Save segments to file...")
        saveButton.connect("clicked", self.saveButtonClicked)

        toolBox = [generateButton, clearButton, openButton, saveButton, self.animatedCheckBox, algoButton]

        super(MainWindowGui, self).__init__(toolBox, "Lab 4 - monotonic polygon triangulation", *args, **kwargs)

        self.segments = []
        self.intersections = []
        self.prev_point = None

    def clearClicked(self, widget, data=None):
        self.clear_figures()
        self.prev_point = None
        self.segments = []

    def algoClicked(self, widget, data=None):
        for f in list(map(lambda i: i.intersection_point, self.intersections)):
            self.remove_figure(f, False)
        self.update_figures()
        time_start = time.time()
        _, intersections = shamos_hoey_intersections(self.segments, self if self.animated else None)
        time_end = time.time()
        if not self.animated:
            for f in list(map(lambda i: i.intersection_point, intersections)):
                self.add_figure(f)
            self.update_figures()
        self.intersections = intersections
        AlgorithmResultsGUI(intersections, time_end - time_start)

    def openButtonClicked(self, widget, data=None):
        self.clearClicked(None)
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Load segments from CSV...", action=gtk.FILE_CHOOSER_ACTION_OPEN,
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
                    if isinstance(f, Line):
                        self.add_figure(f)
                        self.add_figure(f.point1)
                        self.add_figure(f.point2)
                        self.segments.append(f)
            chooser.destroy()
            self.update_figures()
        finally:
            chooser.destroy()

    def saveButtonClicked(self, widget, data=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Save segments to CSV...", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        chooser.set_current_folder(path)
        chooser.set_current_name("segments.csv")
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
                save_to_file(chooser.get_filename(), self.segments)
        finally:
            chooser.destroy()

    def generateClicked(self, widget, data=None):
        gui = GenerateGui(self)
        gui.show_all()

    def animatedClicked(self, widget, data=None):
        self.animated = not self.animated

    def handle_click(self, event):
        button = event.button
        if button == 1:
            new_point = Point(event.xdata, event.ydata, 'r')
            prev_point = self.prev_point
            self.add_figure(new_point)
            if prev_point:
                if prev_point.x > new_point.x:
                    (prev_point, new_point) = (new_point, prev_point)
                line = Line.from_points(prev_point, new_point, 'r')
                self.add_figure(line)
                self.segments.append(line)
                self.prev_point = None
            else:
                self.prev_point = new_point
            self.update_figures()
            self.wait(0.05)
