# coding=utf-8

from .comparators import above_y, below_y, is_below_or_same_y, higher_y_then_lower_x_annotated
from .orient import orient
from gui.primitives import Point, Polygon

__author__ = 'Michał Ciołczyk'

(START, END, SPLIT, MERGE, REGULAR) = (0, 1, 2, 3, 4)
(_LEFT, _RIGHT) = (5, 6)

_colors = {
    0: 'green',
    1: 'red',
    2: 'cyan',
    3: 'blue',
    4: 'brown'
}


def _index(index, max_len):
    if index < 0:
        return index + max_len
    elif index >= max_len:
        return index % max_len
    else:
        return index


def is_y_monotonic(polygon):
    highest_y_point_index = reduce(lambda acc, x: acc if polygon.points[acc].y > polygon.points[x].y else x,
                                   range(1, len(polygon.points)), 0)
    lowest_y_point_index = reduce(lambda acc, x: acc if polygon.points[acc].y < polygon.points[x].y else x,
                                  range(1, len(polygon.points)), 0)

    point = polygon.points[lowest_y_point_index]
    end_point = polygon.points[highest_y_point_index]

    points_len = len(polygon.points)

    i = 1
    while point != end_point:
        index = _index(lowest_y_point_index + i, points_len)
        new_point = polygon.points[index]
        if new_point.y < point.y:
            return False
        point = new_point
        i += 1

    point = polygon.points[lowest_y_point_index]
    i = -1
    while point != end_point:
        index = _index(lowest_y_point_index + i, points_len)
        new_point = polygon.points[index]
        if new_point.y < point.y:
            return False
        point = new_point
        i -= 1

    return True


def _classify_point(point, prev_point, next_point, basic_orientation):
    if basic_orientation > 0:
        (prev_point, next_point) = (next_point, prev_point)
    orientation = orient(prev_point, point, next_point)
    if below_y(point, prev_point) and below_y(point, next_point):
        if orientation > 0:
            return END
        else:
            return MERGE
    elif above_y(point, prev_point) and above_y(point, next_point):
        if orientation > 0:
            return START
        else:
            return SPLIT
    else:
        return REGULAR


def classify_polygon(polygon):
    points_len = len(polygon.points)
    points = []
    classifications = []

    # Check for polygon orientation
    basic_orientation = 0
    for i in range(points_len):
        next_index = _index(i + 1, points_len)
        point = polygon.points[i]
        next_point = polygon.points[next_index]
        basic_orientation += (next_point.x - point.x) * (next_point.y + point.y)

    for i in range(points_len):
        point = polygon.points[i]
        prev_index = _index(i - 1, points_len)
        prev_point = polygon.points[prev_index]
        next_index = _index(i + 1, points_len)
        next_point = polygon.points[next_index]
        classification = _classify_point(point, prev_point, next_point, basic_orientation)
        color = _colors[classification]
        points.append(Point(point.x, point.y, color))
        classifications.append(classification)
    return classifications, points


def _divide_polygon(polygon, basic_orientation):
    highest_y_index = reduce(lambda acc, x: acc if polygon.points[acc].y > polygon.points[x].y else x,
                             range(1, len(polygon.points)), 0)
    left = []
    right = []
    points_len = len(polygon.points)
    current_index = highest_y_index
    current_lowest = polygon.points[current_index]
    left.append(current_lowest)
    current_index = _index(current_index + 1, points_len)
    next_point = polygon.points[current_index]

    while is_below_or_same_y(next_point, current_lowest):
        current_lowest = next_point
        left.append(current_lowest)
        current_index = _index(current_index + 1, points_len)
        next_point = polygon.points[current_index]

    last_left_point = _index(current_index - 1, points_len)
    current_index = _index(highest_y_index - 1, points_len)

    while current_index != last_left_point:
        right.append(polygon.points[current_index])
        current_index = _index(current_index - 1, points_len)

    if basic_orientation < 0:
        return left, right
    else:
        return right, left


def _triangle(a, b, c, color='black'):
    return Polygon([a, b, c], color)


def _is_inside(triangle, side):
    [p, q, r] = triangle.points
    orientation = orient(p, q, r)
    return (side == _LEFT and orientation > 0) or (side == _RIGHT and orientation < 0)


def _get_pairs(stack):
    return [(stack[i - 1][0], stack[i][0]) for i in range(len(stack) - 1, 0, -1)]


def triangulate_y_monotonic_polygon(polygon, visualization=None):
    if not is_y_monotonic(polygon):
        raise ValueError("The polygon is not y-monotonic!")

    points_len = len(polygon.points)
    triangles = []

    # Check for polygon orientation
    basic_orientation = 0
    for i in range(points_len):
        next_index = _index(i + 1, points_len)
        point = polygon.points[i]
        next_point = polygon.points[next_index]
        basic_orientation += (next_point.x - point.x) * (next_point.y + point.y)

    left, right = _divide_polygon(polygon, basic_orientation)
    points = sorted([(p, _LEFT) for p in left] + [(p, _RIGHT) for p in right],
                    cmp=higher_y_then_lower_x_annotated)

    stack = [points[0], points[1]]

    for i in range(2, points_len):
        point = points[i]
        top = stack[-1]

        if point[1] != top[1]:
            pairs = _get_pairs(stack)
            for pair in pairs:
                triangle = _triangle(point[0], pair[0], pair[1], 'black')
                triangles.append(triangle)
            stack = [top, point]
        else:
            pairs = _get_pairs(stack)
            last = stack.pop()
            for pair in pairs:
                triangle = _triangle(point[0], pair[0], pair[1], 'black')
                if not _is_inside(triangle, point[1]):
                    break
                triangles.append(triangle)
                last = stack.pop()
            stack.append(last)
            stack.append(point)

    return triangles
