# coding=utf-8
__author__ = 'Michał Ciołczyk'


def is_y_monotonic(polygon):
    highest_y_point_index = reduce(lambda acc, x: acc if polygon.points[acc].y > polygon.points[x].y else x,
                                   range(1, len(polygon.points)), 0)
    lowest_y_point_index = reduce(lambda acc, x: acc if polygon.points[acc].y < polygon.points[x].y else x,
                                  range(1, len(polygon.points)), 0)

    point = polygon.points[lowest_y_point_index]
    end_point = polygon.points[highest_y_point_index]

    i = 1
    while point != end_point:
        index = lowest_y_point_index + i
        if index < 0:
            index += len(polygon.points)
        if index >= len(polygon.points):
            index %= len(polygon.points)
        new_point = polygon.points[index]
        if new_point.y < point.y:
            return False
        point = new_point
        i += 1

    i = -1
    while point != end_point:
        index = lowest_y_point_index + i
        if index < 0:
            index += len(polygon.points)
        if index >= len(polygon.points):
            index %= len(polygon.points)
        new_point = polygon.points[index]
        if new_point.y < point.y:
            return False
        point = new_point
        i -= 1

    return True
