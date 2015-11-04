# coding=utf-8

import gtk

__author__ = 'Michał Ciołczyk'


class AlgorithmResultsGUI(gtk.Window):
    def __init__(self, intersections, time, *args, **kwargs):
        super(AlgorithmResultsGUI, self).__init__(*args, **kwargs)
        self.set_size_request(400, 300)
        table = gtk.Table(3, 1)
        finished_label = gtk.Label('The algorithm has finished. Below are results:')
        table.attach(finished_label, 0, 1, 0, 1)
        intersections_text = self._format_intersections(intersections)
        text_buffer = gtk.TextBuffer()
        text_buffer.set_text('Ran for %s s (including visualization)\n\n'
                             'Found %d intersections:\n\n%s' % (str(time), len(intersections), intersections_text))
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
    def _format_intersections(intersections):
        to_return = ''
        for intersection in intersections:
            segment1 = intersection.segment1
            segment2 = intersection.segment2
            if segment1 > segment2:
                (segment1, segment2) = (segment2, segment1)
            point = intersection.intersection_point
            to_return += '(%s, %s) at (%s, %s)\n' % (str(segment1), str(segment2), str(point.x), str(point.y))
        return to_return

    def _ok_clicked(self, widget, data=None):
        self.destroy()
