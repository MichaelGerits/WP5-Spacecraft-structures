import numpy as np
import math

closingpanelAmount = 6
transversePanelAmount = 2



class StructuralCylinder:
    """
    holds geometry and properties of the structural cylinder
    """
    def __init__(self, R=0, h=0, t=0, E=0, SigmaY=0, rho=0, critical_euler_stress=0, critical_shell_stress=0, Poisson=0, half_waves=2, internal_pressure = 500000):
        self.R = R
        self.h = h
        self.t = t
        self.E = E
        self.SigmaY = SigmaY
        self.rho=rho
        self.Poisson = Poisson
        self.critical_euler_stress = critical_euler_stress
        self.critical_shell_stress = critical_shell_stress
        self.area = self.calcArea()
        self.inertia = self.calcInertia()
        self.mass = self.calcMass()
        self.half_waves = half_waves
        self.internal_pressure = internal_pressure
        pass

    def calcArea(self):
        area = 2 * math.pi * self.R * self.t
        self.area = area
        return area

    def calcMass(self):
        mass = self.area * self.L
        self.mass = mass
        return mass

    def calcInertia(self):
        inertia = math.pi * (self.R ** 3) * self.t
        self.inertia = inertia
        return inertia

#---------------------------------------------------------------------------------------------------------------------------------------------
class TransversePanel:
    """
    holds the geometry and properties of the transverse panels
    """
    def __init__(self, R_outer=0, t_face=0, t_core=0, rho_face=0, rho_core=0, R_struct=0):
        self.R_outer = R_outer
        self.sideLength = R_outer
        self.t_face = t_face
        self.t_core = t_core
        self.rho_face = rho_face
        self.rho_core = rho_core
        self.R_struct = R_struct
        self.holes = [{"r": self.R_struct}] #list of dicts (as to ad positions later if needed)
        self.area =self.calcArea()
        self.mass = self.calcMass()

    def calcArea(self):
        """
        calculates the true area of the plate
        """
        area = (3 * np.sqrt(3))/2 * self.sideLength**2 #area of a hexagon
        for hole in self.holes:
            area -= np.pi*hole["r"]**2
        self.area = area
        return area
    def calcMass(self):
        """
        calculates the mass of the panel
        """
        mass = 2*(self.calcArea()*self.t_face*self.rho_face) + self.calcArea()*self.t_core*self.rho_core
        self.mass = mass
        return mass
#---------------------------------------------------------------------------------------------------------------------------------
class ClosingPanel:
    """
    stores the geometry and properties of A closing panel
    """
    def __init__(self, w=0, h=0, t_face=0, t_core=0, rho_face=0, rho_core=0):
        self.h = h
        self.w = w
        self.t_face = t_face
        self.t_core = t_core
        self.rho_face = rho_face
        self.rho_core = rho_core
        self.holes = []
        self.area = self.calcArea()
        self.mass = self.calcMass()

    def calcArea(self):
        """
        calculates the true area of the panel
        """
        area = self.w * self.h
        for hole in self.holes:
            area -= np.pi*hole["r"]**2
        self.area = area
        return area
    def calcMass(self):
        """
        calculates the mass of the panel
        """
        mass = 2*(self.calcArea()*self.t_face*self.rho_face) + self.calcArea()*self.t_core*self.rho_core
        self.mass = mass
        return mass
    
#--------------------------------------------------------------------------------------------------------
class Attachement:
    """
    stores the geometry and properties of A attachement 
    """
    def __init__(self, pos=np.array(0,0,0), mass=0, fastAmount1 = 2, fastAmount2 = 2):
        self.pos = pos
        self.mass = mass
        self.fastAmount1 = fastAmount1
        self.fastAmount2 = fastAmount2
