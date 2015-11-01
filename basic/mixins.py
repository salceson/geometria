# coding=utf-8
__author__ = 'Michał Ciołczyk'


class OperatorMixin(object):
    def __lt__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return self == other or other < self

    def __le__(self, other):
        return self == other or self < other

    def __ne__(self, other):
        return not self == other

    def __cmp__(self, other):
        if self < other:
            return -1
        elif self == other:
            return 0
        else:
            return 1
