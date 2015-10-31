# coding=utf-8

from __future__ import print_function

import csv

from .primitives import Line, Point

__author__ = 'Michał Ciołczyk'


# noinspection PyBroadException
def load_from_file(filename):
    """Loads data from CSV file and parses them to figures.

    :param filename: path to file to read
    :return: list of parsed figures
    """
    figures = []
    with open(filename, 'rb') as f:
        c = csv.reader(f)
        for row in c:
            fig = row[0]
            if fig == "Line":
                try:
                    label = row[6].strip() if len(row) >= 7 else None
                    x1 = float(row[1].strip())
                    y1 = float(row[2].strip())
                    x2 = float(row[3].strip())
                    y2 = float(row[4].strip())
                    if x1 > x2:
                        (x2, x1) = (x1, x2)
                        (y2, y1) = (y1, y2)
                    if x1 == x2 and x2 == y2:
                        figures.append(Point(x1, y1, row[5].strip(), label))
                    figures.append(Line(x1, y1, x2, y2, row[5].strip(), label))
                except:
                    pass
            elif fig == "Point":
                try:
                    label = row[4].trim() if len(row) >= 5 else None
                    figures.append(Point(float(row[1].strip()), float(row[2].strip()), row[3].strip(), label))
                except:
                    pass
    return figures


def save_to_file(filename, figures):
    """Saves figures to a CSV file.

    :param filename: path to file to save to
    :param figures: list of figures to save
    """
    with open(filename, 'w') as f:
        for fig in figures:
            print(fig.to_csv_line(), file=f)
