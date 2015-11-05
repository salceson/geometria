# coding=utf-8

import gtk

__author__ = 'Michał Ciołczyk'


class AlgorithmResultsGUI(gtk.Window):
    def __init__(self, triangles, time, *args, **kwargs):
        super(AlgorithmResultsGUI, self).__init__(*args, **kwargs)
        self.set_size_request(400, 300)
        self.set_title("Algorithm results")
        table = gtk.Table(3, 1)
        finished_label = gtk.Label('The algorithm has finished. Below are results:')
        table.attach(finished_label, 0, 1, 0, 1)
        triangles_text = self._triangles_text(triangles)
        text_buffer = gtk.TextBuffer()
        text_buffer.set_text('Ran for %s s (including visualization)\n\n'
                             'Split for %d triangles:\n\n%s' % (str(time), len(triangles), triangles_text))
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textarea = gtk.TextView()
        textarea.set_editable(False)
        textarea.set_buffer(text_buffer)
        textarea.set_size_request(400, 200)
        sw.add(textarea)
        table.attach(sw, 0, 1, 1, 2)
        ok_button = gtk.Button("OK")
        ok_button.connect('clicked', self._ok_clicked)
        table.attach(ok_button, 0, 1, 2, 3)
        self.add(table)
        self.show_all()

    @staticmethod
    def _triangles_text(triangles):
        to_return = ''
        for triangle in triangles:
            to_return += "((%f, %f), (%f, %f), (%f, %f))\n" % (
                triangle.points[0].x,
                triangle.points[0].y,
                triangle.points[1].x,
                triangle.points[1].y,
                triangle.points[2].x,
                triangle.points[2].y
            )
        return to_return

    def _ok_clicked(self, widget, data=None):
        self.destroy()
