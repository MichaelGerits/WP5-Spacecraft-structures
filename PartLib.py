import numpy as np
import math
from coordinate_conversion import cylindrical_to_cartesian

closingpanelAmount = 6
transversePanelHeight = 0.7 #m
AttachmentPerPlate = 6



class StructuralCylinder:
    """
    holds geometry and properties of the structural cylinder
    """
    def __init__(self, R=1, h=1.5, t=0, E=110.3e9, SigmaY=980e6, rho=4540, critical_euler_stress=0, critical_shell_stress=0, Poisson=0.32, buckling_k=0, half_waves=0, mass=0):
        self.R = R
        self.h = h
        self.t = t
        self.E = E
        self.SigmaY = SigmaY
        self.rho=rho
        self.Poisson = Poisson
        self.critical_euler_stress = critical_euler_stress
        self.critical_shell_stress = critical_shell_stress
        self.mass = mass
        self.buckling_k = buckling_k
        self.half_waves = half_waves
        pass

#---------------------------------------------------------------------------------------------------------------------------------------------
class TransversePanel:
    """
    holds the geometry and properties of the transverse panels
    """
    def __init__(self, R_outer=1, t_face=0.19805e-3, t_core=15e-3, rho_face=1611, rho_core=48.2, R_struct=0.28, holes=[]):
        self.R_outer = R_outer
        self.sideLength = R_outer
        self.t_face = t_face
        self.t_core = t_core
        self.rho_face = rho_face
        self.rho_core = rho_core
        self.R_struct = R_struct
        self.holes = [{"r": self.R_struct}] + holes #list of dicts (as to ad positions later if needed)
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
    def __init__(self, w=1, h=1.5, t_face=0.19805e-3, t_core=15e-3, rho_face=1611, rho_core=48.2):
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
class Attachment:
    """
    stores the geometry and properties of A attachement
    """
    def __init__(self, pos=np.array([0,0,0]), mass=0.016, fastAmount1 = 2, fastAmount2 = 2, t = 0.001, zload=0, SigmaY=4.14e7, SigmaB=662e6):
        self.pos = np.array(cylindrical_to_cartesian(pos[0], pos[0], pos[0])) #position is in cilindrical coordinates so need to convert
        self.mass = mass
        self.fastAmount1 = fastAmount1 #amount of fasteners on the plate
        self.fastAmount2 = fastAmount2 #amount of fasteners on the cylinder
        self.fastDiameter = 0.005
        self.w = self.fastDiameter * (2 * 2 + 2.5)
        e1 = self.fastDiameter*2
        e2 = self.fastDiameter*2
        self.depth = (2* e2 + 2*self.fastDiameter)


    def CheckBearing(self, cyl):
        """
        This check also includes the thermal stress (calculated manually)
        """
        sigmaTh = 95e6
        result = [1,1]
        for i in range(4):
            P = self.zload/4 * 1.5

            #bearing check for the baseplate thickness
            if P/(self.fastDiameter*self.t) + sigmaTh > self.SigmaB:
                result[0] = 0

            #bearing check for the spacecraft wall
            if P/(self.fastDiameter*cyl.t) + sigmaTh > 1350e6:
                result[1] = 0
        return result
    
    def CheckPullThrough(self):
        """
        checks if the pullthrough passes
        """
        check = []
        for i in range(4):   #iterate through all fastener objects
            areabolthead = (0.008/2)**2 * math.pi - (0.005/2)**2 * math.pi    #calculate area on which compressive stress acts
            sigmay = self.zload/(areabolthead * 4)      #calculate compressive stress
            areat2 = math.pi * 0.008 * self.t   #calculate areas over which the shear stress will act
            areat3 = math.pi * 0.008 * (15e-3+2*0.19805e-3)
            tau2 = self.zload/areat2      #calculate shear stresses
            tau3 = self.zload/areat3
            if areat2 <= areat3:   #calculate von mises stress for greater shear stress
                vonmises = math.sqrt(sigmay**2 + 3 * tau2**2)
            else:
                vonmises = math.sqrt(sigmay**2 + 3 * tau3**2)

            if vonmises < self.sigmaY:  #if vonmises stress is below tensile yield stress, test is passed and add true, if vonmises stress is higher add false to list
                check.append(1)

            else:
                check.append(0)
        
        return check

structuralCylinder = StructuralCylinder(t=0.001, half_waves=1) #TODO: update initial dimensions
