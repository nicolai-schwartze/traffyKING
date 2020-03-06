# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:04:26 2019

@author: Nicolai
"""

import numpy as np
import copy
import pickle
import matplotlib.pyplot as plt

def ConjugateGradientDescent(x, function, epsilon=10**(-3), alpha=0.1, eta=10, h=np.finfo(np.float64).eps): 
    
    d = np.zeros(x.size)
    grad_old = np.ones(x.size)
    eta_opt = eta
    fDynamic = []
    iterationCounter = 0
    saveList = []
    while(np.linalg.norm(grad_old) > epsilon or np.linalg.norm(eta_opt*d) > epsilon):
        grad = numGrad(function, x)
        d = (-1)*grad + ((np.linalg.norm(grad)**2)/(np.linalg.norm(grad_old)**2))*d
        if np.dot(grad, d)/(np.linalg.norm(grad)*np.linalg.norm(d)) > (-1)*alpha:
            d = (-1)*grad
        
        eta_opt = lineSearch(x, d, eta, epsilon, function)
        x = x + eta_opt*(d/np.linalg.norm(d))
        grad_old = grad
        fDynamic.append(function(x))
        
        iterationCounter = iterationCounter + 1
        saveList.append((copy.deepcopy(x), copy.deepcopy(fDynamic)))
        with open('CGD_SaveList.pkl', 'wb') as f:
            pickle.dump(saveList, f)
        print("Iteration: " + str(iterationCounter))
        
    return x, fDynamic


def numGrad(function, x, h=np.finfo(np.float64).eps):
    grad = np.zeros(x.size)
    for i in range(x.size):
        e = np.zeros(x.size)
        e[i] = 1
        dx = h*e
        grad[i] = (function(x+dx) - function(x-dx))/(2*h)
        
    if(np.linalg.norm(grad) == 0.0):
        h = 0.1
        for i in range(x.size):
            e = np.zeros(x.size)
            e[i] = 1
            dx = h*e
            grad[i] = (function(x+dx) - function(x-dx))/(2*h)
        
    return grad


def lineSearch(x, d, eta, epsilon, function):
    phi = 0.618
    d = d/np.linalg.norm(d)
    a = 0
    b = eta
    
    def function2 (t, x=x, d=d, function=function):
        x2 = x + t*d
        return function(x2)
    
    Lambda = a+(1-phi)*(b-a);
    
    fa = function2(Lambda)
    mu = a + (b-a)*phi;
    fb = function2(mu)
    
    while(b-a > epsilon):
        print(b-a)
        if(fa > fb): 
            a = Lambda
            Lambda = mu
            mu = a + (b-a)*phi
            fa = fb
            fb = function2(mu)
        else: 
            b = mu
            mu = Lambda
            Lambda = a + (1-phi)*(b-a);
            fb = fa;
            fa = function2(Lambda)
    
    return (1/2)*(a+b)
    
        


if __name__ == "__main__":
    
    print("start test")
    print(50*"=")
    
    def sphere(x):
        return np.dot(x,x)
    
    print(numGrad(sphere, np.array([1,1])))
    print(lineSearch(np.array([1, 1]), np.array([-1, -1]), 5, 10**-3, sphere))
    opt, fD = ConjugateGradientDescent(np.array([10, -10]), sphere)
    plt.title("conjugate gradient descent on sphere function")
    plt.plot(fD)
    plt.xlabel("iteration")
    plt.ylabel("function value")
    
    print(opt)
