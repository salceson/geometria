# coding=utf-8
from basic.avl_tree import AVLTree

__author__ = 'Michał Ciołczyk'

if __name__ == '__main__':
    avl = AVLTree()
    avl.insert(9)
    avl.insert(5)
    avl.insert(10)
    avl.insert(0)
    avl.insert(6)
    avl.insert(11)
    avl.insert(-1)
    avl.insert(1)
    avl.insert(2)

    print avl.root

    print avl.pre_order()
    print avl.successor(2)
    print avl.predecessor(2)

    avl.delete(10)

    print avl.root

    print avl.pre_order()

    print avl.find(0)
