# coding=utf-8
import time
from project.delaunay_triangulation import triangulate
from project.generators import generate_random
from matplotlib import pyplot as plt
from scipy.interpolate import spline
import numpy as np

__author__ = 'Michał Ciołczyk, Michał Janczykowski'

if __name__ == '__main__':
    methods = ['kirkpatrick', 'brute']
    points_nums = [100, 500, 1000, 5000, 10000]
    results = []
    for method in methods:
        method_results = []
        for points_num in points_nums:
            points = generate_random(points_num, 0, points_num * 10, 0, points_num * 10)
            time_start = time.time()
            triangulate(points, search_struct_name=method)
            time_end = time.time()
            method_results.append(time_end - time_start)
        results.append(method_results)
    print 'Kirkpatrick', results[0]
    print 'Brute', results[1]
    points_nums_arr = np.array(points_nums)
    x_new = np.linspace(100, 10000, 100)
    kirkpatrick = spline(points_nums_arr, np.array(results[0]), x_new)
    brute = spline(points_nums_arr, np.array(results[1]), x_new)
    plt.plot(x_new, kirkpatrick, 'r', label='Kirkpatrick')
    plt.plot(x_new, brute, 'b', label='Brute')
    plt.xlabel('Number of points')
    plt.ylabel('Running time [s]')
    plt.legend(loc='upper left')
    plt.savefig('chart.png')
