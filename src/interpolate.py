# Author: Wyatt Scott
# Date: 1/2022
# Description: Provide functions for linear and quadratic interpolation
# of pump curves
import numpy as np

# Linear interpolation, parameters are two-member lists representing x
# and y coordinates and the input value
def linear(p1,p2,x):

    m = (p2[1] - p1[1]) / (p2[0] - p1[0])

    return p1[1] + m*(x-p1[0])

# Quadratic interpolation, parameters are two-member lists representing
# x and y coordinates and the input value
def quadratic(p1,p2,p3,x):

    a = np.array([[1,p1[0],p1[0]**2], 
                [1,p2[0],p2[0]**2], 
                [1,p3[0],p3[0]**2]])

    b = np.array([p1[1],p2[1],p3[1]])

    sol = np.linalg.solve(a,b)
    
    return sol[0] + sol[1] * x + sol[2] * x**2