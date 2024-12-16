import numpy as np
import math
from PartLib import structuralCylinder as cyl
import PartLib
import Loads
from scipy import optimize

# Task 5.2 sizing primary structure for internal pressure.

# def hoopStress(cylinder):


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

def Buck(arr, fixed):
    E = fixed[0]
    Poisson = fixed[1]
    SigmaY = fixed[2]
    t = arr[0]
    L = arr[1]
    R = arr[2]
    half_waves = arr[3]
    p = Loads.p
    I = math.pi * (R ** 3) * t
    A = 2 * math.pi * R * t
    buckling_Q = bucklingQ(p, E, R, t)
    buckling_k = optimize.minimize(bucklingK, x0=[half_waves], args=[L, R, t, Poisson])
    buckling_k.fun
    zstress = Loads.P[2] / (2 * math.pi * R * t)
    if shellBuckling(E, Poisson, t, L, buckling_Q, buckling_k.fun) > zstress and eulerBuckling(I, E, A, L) > zstress and R / t > SigmaY / p:
        return 2*math.pi*R*L
    else:
        return 500


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
def CalcPanelLoads():
    A = Loads.A
    
def CalcAttachForces():
    return