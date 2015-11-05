# coding=utf-8

import gtk

__author__ = 'Michał Ciołczyk'


class IsMonotonicGUI(gtk.Window):
    def __init__(self, result, time, *args, **kwargs):
        super(IsMonotonicGUI, self).__init__(*args, **kwargs)
        self.set_size_request(400, 150)
        self.set_title("Information")
        table = gtk.Table(2, 1)
        text = 'The polygon %s y-monotonic.\n\n' \
               'Algorithm ran for %f s.' % ('is' if result else "isn't", time)
        finished_label = gtk.Label(text)
        table.attach(finished_label, 0, 1, 0, 1)
        ok_button = gtk.Button("OK")
        ok_button.connect('clicked', self._ok_clicked)
        table.attach(ok_button, 0, 1, 1, 2)
        self.add(table)
        self.show_all()

    def _ok_clicked(self, widget, data=None):
        self.destroy()
