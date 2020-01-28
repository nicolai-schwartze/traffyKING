# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 23:33:44 2020

@author: Nicolai
----------------
"""


from __future__ import absolute_import
from __future__ import print_function

import sys
import pickle
import numpy as np

sys.path.append('../../Modules')
import CGD

import Cross_3_3_day as c33


if __name__ == "__main__":
    
    # calculating
    # print("start init random")
    # x = np.array([90, 0, 5, 10, 15, 20, 25, 30, 35, 40])
    # print("read old pop")
    # with open('CGD_SaveList.pkl', 'rb') as pickle_file:
    #     backup = pickle.load(pickle_file)
    # x = backup[-1][0]
    # print("finished init")
    # opt4, fD4 = CGD.ConjugateGradientDescent(x, c33.function_Cross_3_3, epsilon=10**(-1))
