# coding=utf-8
import gtk
import os
import time

from gui.file_utils import load_from_file, save_to_file
from gui.primitives import Point
from gui.gui_with_canvas_and_toolbar import GuiWithCanvasAndToolbar
from project.algorithm_results import AlgorithmResultsGUI
from project.delaunay_triangulation import triangulate
from project.generate_gui import GenerateGui

__author__ = 'Michał Ciołczyk'


# noinspection PyBroadException,PyPep8Naming
class MainWindowGui(GuiWithCanvasAndToolbar):
    def __init__(self, *args, **kwargs):
        infoLabel = gtk.Label("Draw points by pressing\nleft mouse button.")
        clearButton = gtk.Button("Clear")
        clearButton.connect("clicked", self.clearClicked)
        generateButton = gtk.Button("Generate data...")
        generateButton.connect("clicked", self.generateClicked)
        methodLabel = gtk.Label("Method:")
        methodRadio1 = gtk.RadioButton(None, "Kirkpatrick")
        methodRadio1.connect("toggled", self.methodChanged, "kirkpatrick")
        methodRadio2 = gtk.RadioButton(methodRadio1, "Brute")
        methodRadio2.connect("toggled", self.methodChanged, "brute")
        self.method = "kirkpatrick"
        animatedCheckBox = gtk.CheckButton("Animated")
        animatedCheckBox.connect("clicked", self.animatedClicked)
        self.animated = False
        trianglesCheckBox = gtk.CheckButton("Draw result triangles")
        trianglesCheckBox.set_active(True)
        trianglesCheckBox.connect("clicked", self.trianglesClicked)
        self.triangles = True
        algoButton = gtk.Button("Triangulate")
        algoButton.connect("clicked", self.algoClicked)
        openButton = gtk.Button("Load points from file...")
        openButton.connect("clicked", self.openButtonClicked)
        saveButton = gtk.Button("Save points to file...")
        saveButton.connect("clicked", self.saveButtonClicked)

        toolBox = [infoLabel, clearButton, openButton, saveButton, generateButton, methodLabel,
                   methodRadio1, methodRadio2, animatedCheckBox, trianglesCheckBox, algoButton]

        super(MainWindowGui, self).__init__(toolBox, "Project - Delaunay triangulation", False, *args, **kwargs)

        self.points = []

    def clearClicked(self, widget, data=None):
        self.clear_figures()
        self.points = []

    def algoClicked(self, widget, data=None):
        try:
            if self.triangles:
                self.clear_figures()
                self.add_all_figures(self.points)
                self.update_figures()
            time_start = time.time()
            triangles = triangulate(self.points, visualization=self if self.animated and self.triangles else None)
            time_end = time.time()
            if self.triangles:
                self.add_all_figures(triangles)
                self.update_figures()
            AlgorithmResultsGUI(triangles, time_end - time_start)
        except ValueError as e:
            print e

    def openButtonClicked(self, widget, data=None):
        self.clearClicked(None)
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Load points from CSV...", action=gtk.FILE_CHOOSER_ACTION_OPEN,
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
                    if isinstance(f, Point):
                        self.add_figure(f)
                        self.points.append(f)
            self.update_figures()
        finally:
            chooser.destroy()

    def saveButtonClicked(self, widget, data=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chooser = gtk.FileChooserDialog(title="Save points to CSV...", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        chooser.set_current_folder(path)
        chooser.set_current_name("points.csv")
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
                save_to_file(chooser.get_filename(), self.points)
        finally:
            chooser.destroy()

    def animatedClicked(self, widget, data=None):
        self.animated = not self.animated

    def trianglesClicked(self, widget, data=None):
        self.triangles = not self.triangles

    def generateClicked(self, widget, data=None):
        gui = GenerateGui(self)
        gui.show_all()

    def methodChanged(self, widget, data):
        if widget.get_active():
            self.method = str(data)

    def handle_click(self, event):
        button = event.button

        if not event.xdata or not event.ydata:
            return

        if button == 1:
            new_point = Point(event.xdata, event.ydata, 'black')
            self.add_figure(new_point)
            self.points.append(new_point)
            self.update_figures()
            self.wait(0.05)
