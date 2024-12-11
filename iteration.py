import Main
import numpy as np
import PartLib
import Loads
import math
from coordinate_conversion import cylindrical_to_cartesian

structuralCylinder = PartLib.StructuralCylinder(R=12) #TODO: update initial dimensions

if Main.eulerBuckling(structuralCylinder) < Loads.P[2]/(2*math.pi*structuralCylinder.R*structuralCylinder.t):
    print("Fail")


#allocates the initial lists
#----------------------------------------------------------------------------------------------------------------------------------
closePanelList = [PartLib.ClosingPanel(w=1, h=1.5)] * PartLib.closingpanelAmount
transversePanelList = [PartLib.TransversePanel(R_outer=1)] * 2 #TODO: add initial dimensions
Attachments = []
angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

for i in range(PartLib.AttachmentPerPlate, step=2): #assign the positions
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]))) #lower plate
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]))) #upper plate
#-----------------------------------------------------------------------------------------------------------------------------------