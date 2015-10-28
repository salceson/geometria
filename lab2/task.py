# coding=utf-8
import os

__author__ = 'Michał Ciołczyk'


for set in ['a', 'b', 'c', 'd']:
    for method in ['g', 'j']:
        os.system('python generate_outputs.py %s %s' % (set, method))
