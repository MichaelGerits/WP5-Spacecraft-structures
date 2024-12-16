import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian

# Main.hoopStress(structuralCylinder) #gets the thickness by pressure calculation
#
# if Main.eulerBuckling(structuralCylinder) < Loads.P[2]/structuralCylinder.calcArea():
#     print("Fail by Euler Buckling")
#
# if Main.shellBuckling(structuralCylinder) < Loads.P[2]/structuralCylinder.calcArea():
#     print("Fail by Shell Buckling")


#optimising for buckling (its scuffed)
Resulto_Buck = optimize.minimize(Main.Buck, [structuralCylinder.t, structuralCylinder.R, structuralCylinder.half_waves], args=[structuralCylinder.E, structuralCylinder.Poisson, structuralCylinder.SigmaY, structuralCylinder.h], bounds=optimize.Bounds([0.001, 0.001, 0.001], [0.1, 1, 100]))
print(Resulto_Buck) #prints the results of the optimiser
structuralCylinder.mass = structuralCylinder.rho * Resulto_Buck.fun #the function output volume, so the mass is the output(.fun) times density

# updates structuralCylinder with the values given by the optimiser
structuralCylinder.t = Resulto_Buck.x[0]
structuralCylinder.R = Resulto_Buck.x[1]
structuralCylinder.half_waves = Resulto_Buck.x[2]

#final check just to make sure
print(f"t = {structuralCylinder.t} m, R = {structuralCylinder.R} m")

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

Panel1Mass = [] #list of masses on the first transverse panel
Panel2Mass = [] #list of masses on the second transverse panel

