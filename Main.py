import numpy as np
import math
import scipy
import PartLib

# Task 5.2 sizing primary structure for internal pressure.

# Task 5.3 buckling

def EulerBuckling(E, I, A, L):
    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    return critical_euler_stress

def BucklingK(L, R, t1, Poisson, half_waves):
    buckling_k = half_waves + (12 * (L ** 4) * (1 - (Poisson ** 2)))/((math.pi ** 4) * (R ** 2) * (t1 ** 2) * half_waves)
    return buckling_k