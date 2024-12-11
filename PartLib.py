import numpy as np

class StructuralCylinder:
    def __init__(self, R=0, h=0, t=0, E=0, SigmaY=0, rho=0):
        self.R = R
        self.h = h
        self.t = t
        self.E = E
        self.SigmaY = SigmaY
        pass

class TransversePanel:
    def __init__(self, R_outer=0, t_face=0, t_core=0, rho_face=0, rho_core=0, R_struct=0):
        self.R_outer = R_outer
        self.sideLength = R_outer
        self.t_face = t_face
        self.t_core = t_core
        self.rho_face = rho_face
        self.rho_core = rho_core
        self.R_struct = R_struct
        self.holes = [{"r": self.R_struct}]
        self.area =(3 * np.sqrt(3))/2 * self.sideLength**2
    def calcArea(self):
        area = (3 * np.sqrt(3))/2 * self.sideLength**2
        for hole in self.holes:
            area -= np.pi*hole["r"]**2
            #TODO:add positions
    def calcMass(self):
        mass = 2*(self.area*self.t_face*self.rho_face) + self.area*self.t_core*self.rho_core
        self.mass = mass
        return mass
    
class ClosingPanel:
    def __init__(self, w=0, t_face=0, t_core=0, rho_face=0, rho_core=0):
        self.R_outer = R_outer
        self.sideLength = R_outer
        self.t_face = t_face
        self.t_core = t_core
        self.rho_face = rho_face
        self.rho_core = rho_core
        self.area =(3 * np.sqrt(3))/2 * self.sideLength**2
    def calcMass(self):
        mass = 2*(self.area*self.t_face*self.rho_face) + self.area*self.t_core*self.rho_core
        self.mass = mass
        return mass