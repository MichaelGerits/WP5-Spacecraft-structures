import numpy as np
import math
import scipy
import PartLib

# Task 5.2 sizing primary structure for internal pressure.

# Task 5.3 buckling

def eulerBuckling(E, I, A, L):
    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    return critical_euler_stress

def bucklingK(L, R, t1, Poisson, half_waves):
    buckling_k = half_waves + (12 * (L ** 4) * (1 - (Poisson ** 2)))/((math.pi ** 4) * (R ** 2) * (t1 ** 2) * half_waves)
    return buckling_k

def bucklingQ(p, E, R, t1):
    buckling_Q = (p/E) * (R/t1)**2
    return buckling_Q

def shellBuckling(buckling_Q, buckling_k, E, Poisson, t1, L):
    coefficient = 1.983 - 0.983*math.exp(-23.14*buckling_Q)
    ratio1 = ((math.pi **2)*E)/(12*(1 - (Poisson**2)))
    ratio2 = (t1/L)**2
    critical_shell_stress = coefficient * buckling_k * ratio1 * ratio2
    return critical_shell_stress