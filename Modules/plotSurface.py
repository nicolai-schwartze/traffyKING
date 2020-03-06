# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

def singleSphere(x):
    return np.dot(x,x)
    
def multiSphere (x): 
    r1 = singleSphere(x - 4)
    r2 = singleSphere(x + 4)
    return [r1, r2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.arange(-30, 30, 0.1)
X, Y = np.meshgrid(x, y)

zs0 = np.array([multiSphere(np.array([x,y]))[0] for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs0.reshape(X.shape)
ax.plot_surface(X, Y, Z, cmap=cm.gnuplot)

zs1 = np.array([multiSphere(np.array([x,y]))[1] for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs1.reshape(X.shape)
ax.plot_surface(X, Y, Z, cmap=cm.gnuplot)


plt.title("multi shpere test function")
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("f(X1,X2)")
plt.savefig("multiSphere.pdf")
plt.show()
  