import numpy as np
import math
import scipy
from PartLib import structuralCylinder as cyl
import PartLib
import Loads

# Task 5.2 sizing primary structure for internal pressure.

def hoopStress(cylinder):
    cylinder.t =  Loads.p * cylinder.R / cylinder.SigmaY

# Task 5.3 buckling

def eulerBuckling(cylinder):
    I = cylinder.calcInertia()
    E = cylinder.E
    A = cylinder.calcArea()
    L = cylinder.h

    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    return critical_euler_stress

buckling_k_arr = np.array([cyl.h, cyl.R, cyl.t, cyl.Poisson, cyl.half_waves])
def bucklingK(buckling_k_arr):
    L = buckling_k_arr[0]
    R = buckling_k_arr[1]
    t = buckling_k_arr[2]
    Poisson = buckling_k_arr[3]
    half_waves = buckling_k_arr[4]

    buckling_k = half_waves + (12 * (L ** 4) * (1 - (Poisson ** 2)))/((math.pi ** 4) * (R ** 2) * (t ** 2) * half_waves)
    return buckling_k

def bucklingQ(cylinder):
    p = cylinder.p
    E = cylinder.E
    R = cylinder.R
    t = cylinder.t

    buckling_Q = (p/E) * (R/t)**2
    return buckling_Q

def shellBuckling(cylinder):
    E = cylinder.E
    Poisson = cylinder.Poisson
    t = cylinder.t
    L = cylinder.h
    buckling_Q = bucklingQ(cylinder)
    buckling_k = bucklingK(cylinder)

    coefficient = 1.983 - 0.983*math.exp(-23.14*buckling_Q)
    ratio1 = ((math.pi **2)*E)/(12*(1 - (Poisson**2)))
    ratio2 = (t/L)**2
    critical_shell_stress = coefficient * buckling_k * ratio1 * ratio2
    return critical_shell_stress

#5.4----------------------------------------------------------------------------
def CalcMass(panels, attach):
    panelMass = 0
    for panel in panels:
        panelMass += panel.calcMass()

    attachMass = 0
    for att in attach:
        attachMass += att.mass

    return panelMass + attachMass