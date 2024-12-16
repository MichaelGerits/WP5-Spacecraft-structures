import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian

if Main.eulerBuckling(structuralCylinder) < Loads.zstress:
    print("Fail")

MichaelsBaneResultoOfLambda = optimize.minimize(Main.bucklingK, [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, structuralCylinder.half_waves], bounds=optimize.Bounds([structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 0], [structuralCylinder.h, structuralCylinder.R, structuralCylinder.t, structuralCylinder.Poisson, 100]))
print(MichaelsBaneResultoOfLambda)
#allocates the initial lists
#----------------------------------------------------------------------------------------------------------------------------------
closePanelList = [PartLib.ClosingPanel(w=1, h=1.5)] * PartLib.closingpanelAmount
transversePanelList = [PartLib.TransversePanel(R_outer=1)] * 2 #TODO: add initial dimensions
Attachments = []
angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

for i in range(1, PartLib.AttachmentPerPlate, 2): #assign the positions
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]))) #lower plate
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]))) #upper plate
#-----------------------------------------------------------------------------------------------------------------------------------