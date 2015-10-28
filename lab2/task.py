# coding=utf-8
import os

__author__ = 'Michał Ciołczyk'


NO_ANIM = True

for set in ['a', 'b', 'c', 'd']:
    for method in ['g', 'j']:
        python_script = 'generate_outputs_no_anim.py' if NO_ANIM else 'generate_outputs.py'
        os.system('python %s %s %s' % (python_script, set, method))
