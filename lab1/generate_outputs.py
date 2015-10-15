# coding=utf-8

import sys
import os

__author__ = 'Michał Ciołczyk'

filename = sys.argv[1]
n = sys.argv[2]

to_call = [
    ['a', 'myorient2d'],
    ['b', 'orient2dfast'],
    ['c', 'orient2dexact'],
    ['d', 'orient2dslow']
]

os.system('python visualize.py ' + filename + ' 0 0')

for [letter, func] in to_call:
    filename_out = filename[:-3] + '_' + letter + '.out'
    os.system('./lab1 orient ' + func + ' ' + str(n) + ' -1 0 1 0.1 ' + filename + ' ' + filename_out)
    os.system('python visualize.py ' + filename_out + ' 1 0')
