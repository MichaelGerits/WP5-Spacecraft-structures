import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian

structuralCylinder = PartLib.StructuralCylinder() #TODO: update initial dimensions

Main.hoopStress(structuralCylinder) #gets the thickness by pressure calculation
if Main.eulerBuckling(structuralCylinder) < Loads.P[2]/(2*math.pi*structuralCylinder.R*structuralCylinder.t):
    print("Fail")

MichaelsBaneResultoOfLambda = optimize.minimize(Main.bucklingK, [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, structuralCylinder.half_waves], bounds=optimize.Bounds([structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 0], [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 100]))
print(MichaelsBaneResultoOfLambda)
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