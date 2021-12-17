# Author: Wyatt Scott
# Date: 12/2021
# Description: Pipe system object that accounts for head loss in both laminar
# and turbulent flows and has graphing functionalities

import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

class PipeSystem:
    
    # Computational parameters
    lensection = 0.001

    # Physical properties
    mu = 1e-3 # viscosity of water in SI units
    rho = 998 # density of water in SI units
    g = 9.81 # acceleration due to gravity

    # Component dictionary
    comptypes = {
        # TODO: Fill components and loss coefficients
        'None': 0,
        'End': 0 # TODO: Find real value
    }

    # Material roughness dictionary
    mattypes = {
        # TODO: Fill
        'dummy': 0.005
    }

    # Constructor
    def __init__(self,material,diameter):

        # Pipe characteristics
        self.epsilon = self.mattypes[material]
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
    def addSection(self,length,deltaz,firstcomp):

        # Error checking
        if (length < 0):
            raise Exception('Length can\'t be negative.')
        elif (length < abs(deltaz)):
            raise Exception('The elevation can\'t change more than the length.')

        nvals = int(length / self.lensection + 1)

        if (self.pos == []):

            self.pos = np.arange(0,length,self.lensection)

            self.z = np.arange(0,deltaz,self.lensection)

            self.p = np.zeros(nvals)

            self.KL = np.zeros(nvals)
            self.KL[0] = self.comptypes[firstcomp]
            self.KL[len(self.KL)-1] = self.comptypes['End']

        else:

            lastpos = self.pos[len(self.pos)-1]
            newpos = np.arange(lastpos,length+lastpos,self.lensection)
            self.pos = np.hstack((self.pos[:(len(self.pos)-1)],newpos))

            lastz = self.z[len(self.z)-1]
            newz = np.arange(lastz,deltaz+lastz,self.lensection)
            self.z = np.hstack((self.z[:(len(self.z)-1)],newz))

            self.p = np.hstack((self.p[:(len(self.p)-1)],np.zeros(nvals)))

            newKL = np.zeros(nvals)
            newKL[0] = firstcomp
            newKL[len(newKL)-1] = comptypes['End']
            self.KL = np.hstack((self.KL[:(len(self.KL)-1)],newKL))


    def solve(self):
        # TODO: Implement

        return



    # Helper member functions

    def findV(self):
        return

    def findP(self):
        return

    def fLam(self):
        return 64 / self.Re

    def fTurb(self):
        # TODO: Implement
        return 

def main():
    
    system = PipeSystem('dummy',0.5)
    system.addSection(2.0,1.5,'None')

    print(system.pos)
    print(system.z)
    print(system.p)
    print(system.KL)

if __name__ == "__main__":
    main()