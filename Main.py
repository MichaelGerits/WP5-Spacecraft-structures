import numpy as np
import math
import scipy
import PartLib

# Task 5.2 sizing primary structure for internal pressure.

def hoopStress(cylinder):
    cylinder.t = cylinder.internal_pressure * cylinder.R / cylinder.SigmaY

# Task 5.3 buckling

def eulerBuckling(cylinder):
    I = cylinder.calcInertia()
    E = cylinder.E
    A = cylinder.calcArea()
    L = cylinder.h

    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    cylinder.critical_euler_stress = critical_euler_stress

def bucklingK(cylinder):
    L = cylinder.h
    R = cylinder.R
    t = cylinder.t
    Poisson = cylinder.Poisson
    half_waves = cylinder.walf_waves

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
    cylinder.critical_shell_stress = critical_shell_stress