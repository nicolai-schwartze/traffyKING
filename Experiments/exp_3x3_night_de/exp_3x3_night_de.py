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
import DE

import Cross_3_3_night as c33


if __name__ == "__main__":
    
    # calculating
    print("start init random")
    pop = np.random.rand(20,2)*np.random.randint(5, 70)
    # print("read old pop")
    # with open('DE_SaveList.pkl', 'rb') as pickle_file:
    #     backup = pickle.load(pickle_file)
    # pop = backup[-1][0]
    print("finished init")
    opt4, fD4 = DE.DifferentialEvolution(pop, c33.function_Cross_3_3)
