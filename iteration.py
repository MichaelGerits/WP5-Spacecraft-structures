import Main
import numpy as np
import PartLib
import Loads
import math
from scipy import optimize

structuralCylinder = PartLib.StructuralCylinder(R=12) #TODO: update initial dimensions

if Main.eulerBuckling(structuralCylinder) < Loads.zstress:
    print("Fail")

MichaelsBaneResultoOfLambda = optimize.minimize()

#allocates the initial transverse and closing panels as a list
closePanelList = [PartLib.ClosingPanel()] * PartLib.closingpanelAmount #TODO: add initial dimensions
transversePanelList = [PartLib.TransversePanel()] * PartLib.transversePanelAmount #TODO: add initial dimensions