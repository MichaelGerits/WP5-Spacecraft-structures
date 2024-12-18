import numpy as np
import math
from PartLib import structuralCylinder as cyl
import PartLib
import Loads
from scipy import optimize


# hoop stress

# Task 5.3 buckling

def eulerBuckling(I, E, A, L):
    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    return critical_euler_stress

buckling_k_arr = np.array([cyl.h, cyl.R, cyl.t, cyl.Poisson, cyl.half_waves])
def bucklingK(arr, fixed):
    L = fixed[0]
    R = fixed[1]
    t = fixed[2]
    Poisson = fixed[3]
    half_waves = arr[0]

    buckling_k = half_waves + (12 * (L ** 4) * (1 - (Poisson ** 2)))/((math.pi ** 4) * (R ** 2) * (t ** 2) * half_waves)
    return buckling_k

def bucklingQ(p, E, R, t):
    buckling_Q = (p/E) * (R/t)**2
    return buckling_Q

def shellBuckling(E, Poisson, t, L, buckling_Q, buckling_k):
    coefficient = 1.983 - 0.983*math.exp(-23.14*buckling_Q)
    ratio1 = ((math.pi **2)*E)/(12*(1 - (Poisson**2)))
    ratio2 = (t/L)**2
    critical_shell_stress = coefficient * buckling_k * ratio1 * ratio2
    return critical_shell_stress

def Buck(arr, fixed): #optimises the structural cylinder

    #fixed material properties, not optimised
    E = fixed[0]
    Poisson = fixed[1]
    SigmaY = fixed[2]
    L = fixed[3]
    p = Loads.p
    P = Loads.P[2]

    # Geometric properties, will be optimised
    t = arr[0]
    R = arr[1]

    #Some more (geometric) properties
    I = math.pi * (R ** 3) * t
    A = 2 * math.pi * R * t
    buckling_Q = bucklingQ(p, E, R, t)
    buckling_k_op = optimize.minimize(bucklingK, x0=[1], args=[L, R, t, Poisson]) #optimises half_waves for minimal buckling_k
    buckling_k = buckling_k_op.fun #takes the optimal value of buckling_k
    zstress = P / (2 * math.pi * R * t)
    if shellBuckling(E, Poisson, t, L, buckling_Q, buckling_k) > zstress and eulerBuckling(I, E, A, L) > zstress and HoopStress(p, R, t) < SigmaY:
        return 2*math.pi*R*L*t # if the geometry works, it outputs the volume (not volume enclosed, but volume of the structure)
    else:
        return 500000 # otherwise it outputs an arbitrary large value


def HoopStress(pressure, radius, thickness):
    stress = (pressure * radius)/thickness
    return stress


#5.4----------------------------------------------------------------------------
def CalcMass(panels, attach):
    panelMass = 0
    for panel in panels:
        panelMass += panel.calcMass()

    attachMass = 0
    for att in attach:
        attachMass += att.mass

    return panelMass + attachMass

#5.5-----------------------------------------------------------------------------------
def CalcPanelLoads(initMass):
    A = Loads.A
    #TODO:need to define which masses act where
    #TODO: divide that load over the attachements
    return (P1, P2)
def CalcAttachForces():
    #TODO: size the attachments on they're independent loads
    return AttPList
    #TODO: divide over the fasteners