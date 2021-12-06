# Author: Wyatt Scott
# Date: 12/2021
# Description: Pipe system object that accounts for head loss in both laminar
# and turbulent flows and has graphing functionalities

import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

class PipeSystem:
    
    # Physical properties
    mu = 1e-3 # viscosity of water in SI units
    rho = 998 # density of water in SI units
    g = 9.81 # acceleration due to gravity

    # Component dictionary
    comptypes = {
        # TODO: Fill components and loss coefficients
        'None': 0
    }

    # Constructor
    def __init__(self,roughness,diameter):

        # Pipe characteristics
        self.epsilon = roughness
        self.D = diameter

        # Arrays that describe properties at various points in the system
        self.pos = []
        self.z = []
        self.p = []
        self.KL = [] # components that could cause minor head loss

        # Other flow characteristics
        self.v = None
        self.Re = None

    # User-called public member functions
    def addSection(self,length,deltaz,firstcomp,secondcomp='None'):
        # TODO: Implement
        return

    def solve(self):
        # TODO: Implement
        return

    # Private member functions
    def __fLam(self):
        return 64 / self.Re

    def __fTurb(self):
        # TODO: Implement
        return 