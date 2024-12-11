import numpy as np

closingpanelAmount = 6
transversePanelAmount = 2



class StructuralCylinder:
    """
    holds geometry and properties of the structural cylinder
    """
    def __init__(self, R=0, h=0, t=0, E=0, SigmaY=0, rho=0):
        self.R = R
        self.h = h
        self.t = t
        self.E = E
        self.SigmaY = SigmaY
        self.rho=rho
        pass
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