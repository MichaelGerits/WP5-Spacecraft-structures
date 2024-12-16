import numpy as np
import math
from PartLib import structuralCylinder

"""
This document includes the loads and force calculations
"""

#resulting force [Px, Py, Pz]
P = [538.6, 538.6, 1795] #N #if a component is zero, take 10% of the total

#resulting Moment [Mx, My, Mz]
T = [430, 0, 129] #Nm

zstress = P[2]/structuralCylinder.calcArea()

p = 5e5