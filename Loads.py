import numpy as np
import math
from PartLib import structuralCylinder

"""
This document includes the loads and force calculations
"""

#resulting force [Px, Py, Pz]
#N #if a component is zero, take 10% of the total
initialTotalMass = 355 + 1085 #inittial mass of the spacecraft without adding the structure
totalMass = initialTotalMass
A = np.array([1.8*9.81,1.8*9.81,6*9.81])
P = A * totalMass
#resulting Moment [Mx, My, Mz]
T = [430, 0, 129] #Nm

p = 5e5

