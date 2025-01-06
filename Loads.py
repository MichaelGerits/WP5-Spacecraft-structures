import numpy as np
import math
from PartLib import structuralCylinder

"""
This document includes the loads and force calculations
"""


#N #if a component is zero, take 10% of the total
initialTotalMass = 129.1 #mass not including what is attached to the 
totalMass = initialTotalMass
acceleration = np.array([1.8*9.81,1.8*9.81,6*9.81])
P = acceleration * totalMass #resulting force [Px, Py, Pz]
print(P)
#resulting Moment [Mx, My, Mz]
T = [430, 0, 129] #Nm

p = 5e5

