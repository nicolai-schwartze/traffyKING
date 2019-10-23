# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:04:26 2019

@author: Nicolai
"""

import numpy as np

def ConjugateGradientDescent(startPosition, function, epsilon=10**(-3), alpha=0.5, h=10**(-3), eta=10): 
    
    
    while(True):
        
    
    return None


def numGrad(function, x, h):
    f1 = 




function [x, points, fkt_values] = CGD(x, epsilon, alpha, h, fkt_name)
eta = 10; 
points = x;
fkt_values = 0;
d = 0;
grad_old = 1;

while(1)
    grad = numericGradient(fkt_name, x, h);
    d = -grad + (norm(grad)^2/norm(grad_old)^2)*d;
    if(grad.*d/(norm(grad)*norm(d)) > -alpha)
        d = -grad;
    end
    [eta_opt, fkt_value] = lineSearch(x, d, eta, fkt_name);
    fkt_values = [fkt_values, fkt_value];
    points = [points,x];
    grad_old = grad;
    norm_d = d/norm(d);
    x = x + eta_opt * norm_d;
    
    if(norm(grad) < epsilon || norm(eta_opt*norm_d) < epsilon)
        break;
    end
end  
fkt_values = fkt_values(2:end);
end