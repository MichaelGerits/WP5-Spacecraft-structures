import numpy as np
import math
from PartLib import structuralCylinder as cyl
import PartLib
import Loads
from scipy import optimize


# hoop stress

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

def HoopStress(pressure, radius, thickness):
    stress = (pressure * radius)/thickness
    return stress

def constrainer(cyl, P):
    listo = [P*0.28/cyl.SigmaY, (math.sqrt(2) * P * 1.5) / (2 * (math.pi)**2 * math.sqrt(cyl.E))]
    print("losto", listo)
    return max(listo)

def Buck(arr, fixed): #optimises the structural cylinder

    #fixed material properties, not optimised
    E = fixed[0]
    Poisson = fixed[1]
    SigmaY = fixed[2]
    L = fixed[3]
    P = fixed[4]
    R = fixed[5]
    p = Loads.p

    # Geometric properties, will be optimised
    t = arr[0]

    #Some more (geometric) properties
    I = math.pi * (R ** 3) * t
    A = 2 * math.pi * R * t
    buckling_Q = bucklingQ(p, E, R, t)
    buckling_k_op = optimize.minimize(bucklingK, x0=[1], args=[L, R, t, Poisson]) #optimises half_waves for minimal buckling_k
    buckling_k = buckling_k_op.fun #takes the optimal value of buckling_k

    # if shellBuckling(E, Poisson, t, L, buckling_Q, buckling_k) > zstress and eulerBuckling(I, E, A, L) > zstress and HoopStress(p, R, t) < SigmaY:
    #     # print(2*math.pi*R*L*t, shellBuckling(E, Poisson, t, L, buckling_Q, buckling_k) - zstress, eulerBuckling(I, E, A, L) - zstress, SigmaY - HoopStress(p, R, t))
    #     return 2*math.pi*R*L*t # if the geometry works, it outputs the volume (not volume enclosed, but volume of the structure)
    # else:
    #     return 5000 # otherwise it outputs an arbitrary large value
    return 2 * math.pi * R * L * t


#5.4----------------------------------------------------------------------------
def CalcMass(panels, attach):
    panelMass = 0
    for panel in panels:
        panelMass += panel.calcMass()

    attachMass = 0
    for att in attach:
        attachMass += att.CalcMass()

    return panelMass + attachMass

#5.5-----------------------------------------------------------------------------------
def CalcPanelLoads(mass1, mass2):
    acc = Loads.acceleration[2]
    loads = [acc*mass1, acc*mass2]
    return loads
def CalcAttachForces(mass1, mass2):
    load1, load2 = CalcPanelLoads(mass1, mass2)
    att1Load = load1/Loads.AttachmentPerPlate
    att2Load = load2/Loads.AttachmentPerPlate
    fuelLoad = 1085/(4*3*2)

    return max(att1Load, att2Load, fuelLoad)


def FindHighestLoadAttch(attachments):
    """
    finds the attachment with the highest load
    """
    z = 0
    att = attachments[0]
    for attach in attachments:
        if attach.zload > z:
            att = attach
            z=attach.zload
    return att

def ItterateAttach(att,attachements):
    """
    itterates the thickness of the attachment such that it passes the test.
    updates the geometry of the attachments
    "att" is the highest loaded attachement
    """
    #bearing check
    checkResult = att.CheckBearing(cyl)
    while 0 in checkResult:
        updateVal = np.abs(np.array(checkResult) - 1) * 0.001
        for i in attachements:
            i.t += updateVal[0]
        cyl.t += updateVal[1]
        checkResult = att.CheckBearing(cyl)

    #pullthrough check
    checkResult = att.CheckPullThrough()
    while 0 in checkResult:
        for i in attachements:
            i.t += 0.0005
        checkResult= att.CheckPullThrough()

