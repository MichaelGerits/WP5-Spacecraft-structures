import numpy as np
import math
import scipy
import PartLib

# Task 5.2 sizing primary structure for internal pressure.

# Task 5.3 buckling

def EulerBuckling(E, I, A, L):
    critical_euler_stress = ((math.pi ** 2) * E * I) / A * (L**2)
    return critical_euler_stress
