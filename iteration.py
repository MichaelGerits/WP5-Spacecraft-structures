import Main
import numpy as np
import PartLib
from coordinate_conversion import cylindrical_to_cartesian

structuralCylinder = PartLib.StructuralCylinder(R=12) #TODO: update initial dimensions

if Main.eulerBuckling(structuralCylinder) > structuralCylinder.sigmacr:
    print("Fail")


#allocates the initial lists
#----------------------------------------------------------------------------------------------------------------------------------
closePanelList = [PartLib.ClosingPanel()] * PartLib.closingpanelAmount #TODO: add initial dimensions
transversePanelList = [PartLib.TransversePanel()] * 2 #TODO: add initial dimensions
Attachments = []
angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

for i in range(PartLib.AttachmentPerPlate, step=2): #assign the positions
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]))) #lower plate
    Attachments.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]))) #upper plate
#-----------------------------------------------------------------------------------------------------------------------------------