import Main
import numpy as np
import PartLib
import Loads
import math

structuralCylinder = PartLib.StructuralCylinder(R=12) #TODO: update initial dimensions

if Main.eulerBuckling(structuralCylinder) < Loads.P[2]/(2*math.pi*structuralCylinder.R*structuralCylinder.t):
    print("Fail")


#allocates the initial transverse and closing panels as a list
closePanelList = [PartLib.ClosingPanel()] * PartLib.closingpanelAmount #TODO: add initial dimensions
transversePanelList = [PartLib.TransversePanel()] * PartLib.transversePanelAmount #TODO: add initial dimensions