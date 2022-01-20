# Author: Wyatt Scott
# Date: 12/2021 - 1/2022
# Description: Pipe system object that accounts for head loss 
# using Hazen-Williams and has graphing functionalities

import numpy as np 
import matplotlib.pyplot as plt

class PipeSystem:
    
    # CLASS VARIABLES

    # Computational parameters
    lensection = 0.001
    nq = 1000

    # Physical properties
    rho = 998 # density of water in SI units
    g = 9.81 # acceleration due to gravity

    # Component dictionary
    comptypes = {
        # TODO: Fill components and loss coefficients
        'None': 0,
        'Entrance': 0.5,
        '90-Degree Elbow': 1.1, # TODO: There are many kinds of this to be implemented
        'Exit': 0 # TODO: Determine whether this is the correct value
    }

    # Material roughness dictionary
    Crough = {
        # TODO: Fill
        'PVC': 150
    }


    # USER-CALLED PUBLIC MEMBER FUNCTIONS

    # Constructor
    def __init__(self,material,diameter,dtank):

        self.dtank = dtank
        self.Qmax = 0
        self.dQ = 0

        # Pipe characteristics
        self.C = self.Crough[material]
        self.D = diameter

        # Arrays that describe properties at various points in the system
        self.pos = []
        self.z = []
        self.p = []
        self.KL = [] # components that could cause minor head loss

        # Other flow characteristics
        self.v = 0
        self.pcurve = []
        self.pospump = 0
        self.hpump = 0

    # Alter the pipe system
    def addSection(self,length,deltaz,firstcomp='None'):

        # Error checking
        if (length < 0):
            raise Exception('Length can\'t be negative.')
        elif (length < abs(deltaz)):
            raise Exception('The elevation can\'t change more than the length.')

        nvals = int(length / self.lensection + 1)

        # Nothing has been added to the system yet
        if (len(self.pos) == 0):

            self.pos = np.linspace(0,length,nvals)

            self.z = np.linspace(0,deltaz,nvals)

            self.p = np.zeros(nvals)

            self.KL = np.zeros(nvals)
            self.KL[0] = self.comptypes[firstcomp]
            self.KL[len(self.KL)-1] = self.comptypes['Exit'] # All flows have end

        else: # Add to an already existing pipe system
            
            lastpos = self.pos[len(self.pos)-1]
            newpos = np.linspace(lastpos,length+lastpos,nvals)
            self.pos = np.hstack((self.pos[:(len(self.pos)-1)],newpos))

            lastz = self.z[len(self.z)-1]
            newz = np.linspace(lastz,deltaz+lastz,nvals)
            self.z = np.hstack((self.z[:(len(self.z)-1)],newz))

            self.p = np.hstack((self.p[:(len(self.p)-1)],np.zeros(nvals)))

            newKL = np.zeros(nvals)
            newKL[0] = self.comptypes[firstcomp]
            newKL[len(newKL)-1] = self.comptypes['Exit']
            self.KL = np.hstack((self.KL[:(len(self.KL)-1)],newKL))

    # The pump curve is a function
    def addPump(self,loc,curve,Qmax):
        self.Qmax = Qmax
        self.dQ = Qmax / self.nq
        self.pcurve = curve
        self.pospump = loc

    # The only function a user will call to solve the system
    def solve(self):
        self.equalCurve()
        self.findP()


    # GRAPHING FUNCTIONS

    # Plots all components of head together
    def plotAllHead(self):

        self.plotPHead(True)
        self.plotVHead(True)
        self.plotZ(True)
        self.plotTotHead(True)

        #self.headAxes()

        plt.show()

    # Velocity head graph
    def plotVHead(self,intotal=False):
        v = self.v * np.ones(len(self.pos))
        plt.plot(self.pos,v/(2*self.g),label='Velocity Head')
        self.headAxes()
        if (not intotal):
            plt.show()

    # Pressure head graph
    def plotPHead(self,intotal=False):
        plt.plot(self.pos,self.p/(self.rho*self.g),label='Pressure Head')
        self.headAxes()
        if (not intotal):
            plt.show()

    # Elevation head graph
    def plotZ(self,intotal=False):
        plt.plot(self.pos,self.z,label='Elevation Head')
        self.headAxes()
        if (not intotal):
            plt.show()
    
    # Total head graph
    def plotTotHead(self,intotal=False):
        htot = self.p/(self.rho*self.g) + self.z + self.v / (2 * self.g)
        plt.plot(self.pos,htot,label='Total Head')
        self.headAxes()
        if (not intotal):
            plt.show()    

    # Label axes + stuff
    def headAxes(self):
        plt.xlabel('Position (m)')
        plt.ylabel('Head (m)')
        plt.legend()
        plt.grid(True,which='both')

    def plotLosses(self):

        Q = self.v * (np.pi * self.D**2 / 4) # Flow rate
        hl = np.zeros(len(self.pos))
        hv = self.v**2 / (2*self.g) # Kinetic energy head

        for i,l in enumerate(self.pos):
            KL = np.sum(self.KL[:i])
            hlmaj = self.hlossMaj(Q,l)

            hl[i] = hlmaj + hv*KL

        plt.plot(self.pos,hl,label='Head Losses')
        self.headAxes()

    # Plot pump and system curves together
    def plotCurves(self):

        nvals = int(self.Qmax / self.dQ + 1)
        Q = np.linspace(0,self.Qmax,nvals)
        pc = np.zeros(len(Q))
        sc = np.zeros(len(Q))
        for i,q in enumerate(Q):
            pc[i] = self.pcurve(q)
            sc[i] = self.syscurve(q)

        plt.plot(Q,pc,label='Pump Curve')
        plt.plot(Q,sc,label='System Curve')

        plt.legend()
        plt.grid(True,which='both')

        plt.xlabel('Flow Rate (m^3/s)')
        plt.ylabel('Head (m)')
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

        plt.show()


    # HELPER MEMBER FUNCTIONS

    # Solve for the velocity by matching with the pump curve
    def equalCurve(self):

        nvals = int(self.Qmax / self.dQ + 1)
        Q = np.linspace(0,self.Qmax,nvals)

        for i,q in enumerate(Q):
            hsys = self.syscurve(q)
            hp = self.pcurve(q)

            if (i == 0 and hsys >= hp):
                raise Exception('Pump isn\'t strong enough.')
            elif (hp == 0):
                raise Exception('Pump not compatible.')

            if (hsys >= hp): # Just beyond the intersection
                self.v = q / (np.pi * self.D**2 / 4)
                self.hpump = hsys
                return

    # With a found velocity and pump head, find pressure at all points
    def findP(self):

        Q = self.v * (np.pi * self.D**2 / 4) # Flow rate
        gamma = self.rho * self.g # Specific gravity
        hv = self.v**2 / (2*self.g) # Kinetic energy head

        for i,p in enumerate(self.p):
            L = self.pos[i]
            KL = np.sum(self.KL[:i])
            hlmaj = self.hlossMaj(Q,L)

            hpump = 0
            if (L > self.pospump): # Add to pressure if above pump
                hpump = self.hpump

            self.p[i] = gamma * (self.dtank-self.z[i]+hpump-hlmaj-hv*(1+KL))
            

    # For finding equality with pump curve
    def syscurve(self,Q):

        delz = self.z[len(self.z)-1] # Difference between out and in
        v = Q / (np.pi * self.D**2 / 4) 
        hv = v**2 / (2*self.g) # Kinetic energy head

        hlmaj = self.hlossMaj(Q,self.pos[len(self.pos)-1]) # Frictional loss

        return delz - self.dtank + hv * (1 + np.sum(self.KL)) + hlmaj


    # Hazen-Williams head loss formulation
    def hlossMaj(self,Q,pos):
        L = self.pos[len(self.pos)-1]
        return 10.67 * Q**1.852 * pos / (self.C**1.852 * self.D**4.8704)

