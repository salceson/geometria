# coding=utf-8
from .operators_mixin import OperatorMixin

__author__ = 'Michał Ciołczyk'


def _identity(x):
    return x


class _Node(OperatorMixin):
    def __init__(self, value, key=_identity, height=1, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.key_func = key
        self.height = height

    @property
    def key(self):
        return self.key_func(self.value)

    def __lt__(self, other):
        return self.key(self.value) < self.key(other.value)

    def __eq__(self, other):
        return self.key(self.value) == self.key(other.value)

    def __getitem__(self, item):
        if item == 0:
            return self.left
        elif item == 1:
            return self.right
        else:
            raise KeyError

    def __repr__(self):
        if self.key_func == _identity:
            return repr(self.value)
        else:
            return '%s: %s' % (repr(self.key), repr(self.value))

    def __str__(self):
        return self.__repr__()


# noinspection PyMethodMayBeStatic
class AVLTree(object):
    def __init__(self, key=_identity):
        self.root = None
        self.key_func = key

    def _height(self, node):
        if not node:
            return 0
        else:
            return node.height

    def _balance(self, node):
        if not node:
            return 0
        else:
            return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1

        return y

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1

        return x

    def _insert(self, node, value):
        if not node:
            return _Node(value)

        key = self.key_func(value)
        comparison = cmp(key, node.key)

        if comparison == 0:
            return node
        elif comparison < 0:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        node.height = max(self._height(node.left), self._height(node.right)) + 1
        balance = self._balance(node)

        if balance > 1 and cmp(key, node.left.key) < 0:
            return self._rotate_right(node)

        if balance < -1 and cmp(key, node.right.key) > 0:
            return self._rotate_left(node)

        if balance > 1 and cmp(key, node.left.key) > 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and cmp(key, node.right.key) < 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def min(self):
        return self._min(self.root)

    def _max(self, node):
        current = node
        while current.right:
            current = current.right
        return current

    def max(self):
        return self._max(self.root)

    def _delete(self, root, value):
        if not root:
            return root

        key = self.key_func(value)
        root_key = root.key
        comparison = cmp(key, root_key)

        if comparison < 0:
            root.left = self._delete(root.left, value)
        elif comparison > 0:
            root.right = self._delete(root.right, value)
        else:
            if not root.left or not root.right:
                temp = root.left if root.left else root.right
                if not temp:
                    root = None
                else:
                    root = temp
            else:
                temp = self._min(root.right)
                root.value = temp.value
                root.right = self._delete(root.right, temp.value)

        if not root:
            return root

        root.height = max(self._height(root.left), self._height(root.right)) + 1
        balance = self._balance(root)

        if balance > 1 and self._balance(root.left) >= 0:
            return self._rotate_right(root)

        if balance > 1 and self._balance(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if balance < -1 and self._balance(root.right) <= 0:
            return self._rotate_left(root)

        if balance < -1 and self._balance(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _pre_order(self, node):
        if node:
            return [repr(node)] + self._pre_order(node.left) + self._pre_order(node.right)
        else:
            return []

    def pre_order(self):
        return ', '.join(self._pre_order(self.root))

    def _in_order(self, node):
        if node:
            return self._in_order(node.left) + [repr(node)] + self._in_order(node.right)
        else:
            return []

    def in_order(self):
        return ', '.join(self._in_order(self.root))

    def _post_order(self, node):
        if node:
            return self._post_order(node.left) + self._post_order(node.right) + [repr(node)]
        else:
            return []

    def post_order(self):
        return ', '.join(self._post_order(self.root))

    def __repr__(self):
        return self.pre_order()

    def __str__(self):
        return self.__repr__()

    def _find(self, node, key):
        if not node:
            return None

        node_key = node.key
        comparison = cmp(key, node_key)

        if comparison < 0:
            return self._find(node.left, key)
        elif comparison > 0:
            return self._find(node.right, key)
        else:
            return node

    def find(self, key):
        found = self._find(self.root, key)
        return found.value if found else None

    def successor(self, key):
        node = self._find(self.root, key)
        if not node:
            return None

        node_key = node.key

        if node.right:
            min = self._min(node.right)
            return min.value if min else None

        root = self.root
        succ = None

        while root:
            root_key = self.key_func(root.value)
            comparison = cmp(node_key, root_key)
            if comparison < 0:
                succ = root
                root = root.left
            elif comparison > 0:
                root = root.right
            else:
                break

        return succ.value if succ else None

    def predecessor(self, key):
        node = self._find(self.root, key)
        if not node:
            return None

        node_key = node.key

        if node.left:
            max = self._max(node.left)
            return max.value if max else None

        root = self.root
        pred = None

        while root:
            root_key = self.key_func(root.value)
            comparison = cmp(node_key, root_key)
            if comparison < 0:
                root = root.left
            elif comparison > 0:
                pred = root
                root = root.right
            else:
                break

        return pred.value if pred else None
