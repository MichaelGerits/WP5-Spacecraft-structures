import numpy as np
import math
from PartLib import structuralCylinder

"""
This document includes the loads and force calculations
"""
volSmall = 0.3259 #volume of a small fuel tank
volLarge = 0.2474 #volume of a large fuel tank
volTot = volSmall+volLarge

#N #if a component is zero, take 10% of the total
initialTotalMass = 129.1 #mass not including what is attached to the 
totalMass = initialTotalMass
A = np.array([1.8*9.81,1.8*9.81,6*9.81])
P = A * totalMass #resulting force [Px, Py, Pz]
#resulting Moment [Mx, My, Mz]
T = [430, 0, 129] #Nm

p = 5e5

