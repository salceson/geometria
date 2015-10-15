# coding=utf-8

import sys
import os
import time

__author__ = 'Michał Ciołczyk'

filename = sys.argv[1]
n = sys.argv[2]

to_call = [
    ['a1', 'myorient2d2'],
    ['a2', 'myorient2d3'],
    ['b', 'orient2dfast'],
    ['c', 'orient2dexact'],
    ['d', 'orient2dslow']
]

os.system('python visualize.py ' + filename + ' 0 0')

print filename
print

for [letter, func] in to_call:
    filename_out = filename[:-3] + '_' + letter + '.out'
    start = time.time()
    os.system('./lab1 orient ' + func + ' ' + str(n) + ' -1 0 1 0.1 ' + filename + ' ' + filename_out)
    end = time.time()
    print 'Function:', func, ' elapsed:', (end-start), 's'
    os.system('python visualize.py ' + filename_out + ' 1 0')

print
