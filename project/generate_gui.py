# coding=utf-8

import gtk

from .generators import generate_random

__author__ = 'Michał Ciołczyk'


# noinspection PyBroadException
class GenerateGui(gtk.Window):
    def __init__(self, main_window, *args, **kwargs):
        super(GenerateGui, self).__init__(*args, **kwargs)
        self.main_window = main_window
        self.set_size_request(400, 300)
        self.set_title("Generate points...")
        self.labels_checked = False

        table = gtk.Table(6, 2)

        n_label = gtk.Label("Points number:")
        table.attach(n_label, 0, 1, 0, 1)
        self.n_entry = gtk.Entry()
        table.attach(self.n_entry, 1, 2, 0, 1)

        x_min_label = gtk.Label("x min:")
        table.attach(x_min_label, 0, 1, 1, 2)
        self.x_min_entry = gtk.Entry()
        table.attach(self.x_min_entry, 1, 2, 1, 2)

        x_max_label = gtk.Label("x max:")
        table.attach(x_max_label, 0, 1, 2, 3)
        self.x_max_entry = gtk.Entry()
        table.attach(self.x_max_entry, 1, 2, 2, 3)

        y_min_label = gtk.Label("y min:")
        table.attach(y_min_label, 0, 1, 3, 4)
        self.y_min_entry = gtk.Entry()
        table.attach(self.y_min_entry, 1, 2, 3, 4)

        y_max_label = gtk.Label("y max:")
        table.attach(y_max_label, 0, 1, 4, 5)
        self.y_max_entry = gtk.Entry()
        table.attach(self.y_max_entry, 1, 2, 4, 5)

        cancel_button = gtk.Button("Cancel")
        cancel_button.connect("clicked", self.cancel_clicked)
        table.attach(cancel_button, 0, 1, 5, 6)

        ok_button = gtk.Button("Generate")
        ok_button.connect("clicked", self.generate_clicked)
        table.attach(ok_button, 1, 2, 5, 6)

        self.add(table)

    def generate_clicked(self, widget, data=None):
        try:
            n = int(self.n_entry.get_text())
            x_min = float(self.x_min_entry.get_text())
            x_max = float(self.x_max_entry.get_text())
            y_min = float(self.y_min_entry.get_text())
            y_max = float(self.y_max_entry.get_text())
            points = generate_random(n, x_min, x_max, y_min, y_max)
            self.main_window.clearClicked(None)
            self.main_window.add_all_figures(points)
            self.main_window.update_figures()
            self.main_window.points = points
        except:
            pass
        finally:
            self.destroy()

    def cancel_clicked(self, widget, data=None):
        self.destroy()
