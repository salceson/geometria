# coding=utf-8
from copy import deepcopy
import heapq

from bintrees import AVLTree

from .comparators import compare_lower_x_first_then_lower_y
from .constants import epsilon
from .intersections import intersects, get_intersection_point
from .mixins import OperatorMixin

__author__ = 'Michał Ciołczyk'

(_SEGMENT_START, _INTERSECTION, _SEGMENT_END) = (0, 1, 2)


class _SegmentId(OperatorMixin):
    def __init__(self, idx, sweep_state):
        self.idx = idx
        self.sweep_state = sweep_state

    def __lt__(self, other):
        return self.sweep_state.get_cross_y_with_sweep_for_segment_id(self) \
               - self.sweep_state.get_cross_y_with_sweep_for_segment_id(other) > 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "SegmentId(%d)" % self.idx

    def __eq__(self, other):
        return self.idx == other.idx


class _Intersection(OperatorMixin):
    def __init__(self, segment1, segment2):
        self.segment1 = segment1
        self.segment2 = segment2

    def __eq__(self, other):
        return (self.segment1 == other.segment1 and self.segment2 == other.segment2) \
               or (self.segment1 == other.segment2 and self.segment2 == other.segment1)

    def __hash__(self):
        return hash(self.segment1) + 31 * hash(self.segment2)

    def __str__(self):
        return "Intersection(%d, %d)" % (self.segment1, self.segment2)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        raise NotImplementedError


class _SweepEvent(OperatorMixin):
    def __init__(self, event_type, point, segment1, segment2):
        self.event_type = event_type
        self.point = point
        self.segment1 = segment1
        self.segment2 = segment2

    @classmethod
    def from_one_segment(cls, event_type, point, segment1):
        return cls(event_type, point, segment1, None)

    @classmethod
    def from_two_segments(cls, event_type, point, segment1, segment2):
        return cls(event_type, point, segment1, segment2)

    def __lt__(self, other):
        return (compare_lower_x_first_then_lower_y(self.point, other.point) or
                (self.point == other.point and self.event_type < other.event_type))

    def __eq__(self, other):
        return self.point == other.point and self.event_type == other.event_type

    def __str__(self):
        event_type = "I" if self.event_type == _INTERSECTION else "B" if self.event_type == _SEGMENT_START else "E"
        end = ", %s" % self.segment2 if self.segment2 else ''
        return "SweepEvent(%s, %s, %s%s)" % (event_type, self.point, self.segment1, end)

    def __repr__(self):
        return self.__str__()


class _SweepState(object):
    def __init__(self, segments, pos_x):
        self.segments = segments
        self.pos_x = pos_x
        self.tree = AVLTree()

    def insert_and_get_new_neighbours(self, new_segment_id):
        new_neighbours = []
        self.tree.insert(new_segment_id, new_segment_id)
        try:
            new_neighbours.append((self.tree.prev_item(new_segment_id)[0], new_segment_id))
        except KeyError:
            pass
        try:
            new_neighbours.append((self.tree.succ_item(new_segment_id)[0], new_segment_id))
        except KeyError:
            pass
        return new_neighbours

    def erase_and_get_new_neighbours(self, segment_id):
        new_neighbours = []
        before = None
        after = None
        try:
            before = self.tree.prev_item(segment_id)[0]
        except KeyError:
            pass
        try:
            after = self.tree.succ_item(segment_id)[0]
        except KeyError:
            pass
        if before and after:
            new_neighbours.append((before, after))
        self.tree.remove(segment_id)
        return new_neighbours

    def swap_and_get_new_neighbours(self, segment1_id, segment2_id):
        pos_x = self.pos_x
        self.pos_x = pos_x - epsilon
        new_neighbours1 = self.erase_and_get_new_neighbours(segment1_id)
        self.pos_x = pos_x + epsilon
        new_neighbours2 = self.insert_and_get_new_neighbours(segment1_id)
        self.pos_x = pos_x

        all_neighbours = new_neighbours1 + new_neighbours2
        new_neighbours = []

        for neighbours in all_neighbours:
            if neighbours != (segment1_id, segment2_id) and neighbours != (segment2_id, segment1_id):
                new_neighbours.append(neighbours)
        return new_neighbours

    def _get_cross_y_with_sweep_for_segment(self, segment):
        segment_dx = segment.x2 - segment.x1
        sweep_dx = self.pos_x - segment.x1
        segment_dy = segment.y2 - segment.y1
        sweep_dy = segment_dy * (sweep_dx / segment_dx)
        return segment.y1 + sweep_dy

    def get_cross_y_with_sweep_for_segment_id(self, segment_id):
        return self._get_cross_y_with_sweep_for_segment(self.segments[segment_id.idx])


def shamos_hoey_intersections(segments, visualization=None):
    if len(segments) == 0:
        return []

    segments = deepcopy(segments)

    for segment in segments:
        if segment.x1 == segment.x2:
            segment.x2 = segment.x2 + epsilon

    state = _SweepState(segments, min(segments, key=lambda x: x.x1))
    intersections = set()
    events = []

    for (i, segment) in enumerate(segments):
        heapq.heappush(events, _SweepEvent.from_one_segment(_SEGMENT_START, segment.point1, _SegmentId(i, state)))
        heapq.heappush(events, _SweepEvent.from_one_segment(_SEGMENT_END, segment.point2, _SegmentId(i, state)))

    while len(events) > 0:
        event = heapq.heappop(events)
        state.pos_x = event.point.x
        new_neighbours = []

        if event.event_type == _SEGMENT_START:
            new_neighbours = state.insert_and_get_new_neighbours(event.segment1)
        elif event.event_type == _SEGMENT_END:
            new_neighbours = state.erase_and_get_new_neighbours(event.segment1)
        elif event.event_type == _INTERSECTION:
            new_neighbours = state.swap_and_get_new_neighbours(event.segment1, event.segment2)

        for neighbours in new_neighbours:
            (segment_id1, segment_id2) = neighbours
            segment1 = segments[segment_id1.idx]
            segment2 = segments[segment_id2.idx]

            if intersects(segment1, segment2):
                if _Intersection(segment_id1.idx, segment_id2.idx) in intersections \
                        or _Intersection(segment_id2.idx, segment_id1.idx) in intersections:
                    continue

                intersection_point = get_intersection_point(segment1, segment2)
                new_event = _SweepEvent.from_two_segments(_INTERSECTION, intersection_point, segment_id1, segment_id2)

                heapq.heappush(events, new_event)

                intersections.add(_Intersection(segment_id1.idx, segment_id2.idx))

    return map(lambda i: (i.segment1, i.segment2), intersections)
