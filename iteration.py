import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian

Main.hoopStress(structuralCylinder) #gets the thickness by pressure calculation

structuralCylinder.critical_euler_stress = Main.eulerBuckling(structuralCylinder)
structuralCylinder.critical_shell_stress = Main.shellBuckling(structuralCylinder)

if structuralCylinder.critical_euler_stress < Loads.P[2]/structuralCylinder.calcArea():
    print("Fail by Euler Buckling")

if structuralCylinder.critical_shell_stress < Loads.P[2]/structuralCylinder.calcArea():
    print("Fail by Shell Buckling")

Resulto_Lambda = optimize.minimize(Main.bucklingK, [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, structuralCylinder.half_waves], bounds=optimize.Bounds([structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 0], [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 100]))
print(Resulto_Lambda)
structuralCylinder.buckling_k = Resulto_Lambda.fun
#allocates the initial lists
#----------------------------------------------------------------------------------------------------------------------------------
closePanelList = [PartLib.ClosingPanel(w=1, h=1.5)] * PartLib.closingpanelAmount
transversePanelList = [PartLib.TransversePanel()] * 2 + [PartLib.TransversePanel(R_struct=0)] #2transverse panels + 1 closing panels
Attachments = [] #initialise list
angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

for i in range(1, PartLib.AttachmentPerPlate, 2): #assign the positions
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]))) #lower plate
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]))) #upper plate
#-----------------------------------------------------------------------------------------------------------------------------------

att_and_panelMass = Main.CalcMass(closePanelList+transversePanelList, Attachments)
