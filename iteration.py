import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian
massdiff = 10
while massdiff >= 1:
    """
    The original Buckling calculations are done assuming that the mass excluding the structural mass is added
    """

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

    #TODO: update attchment objzct to include geometry
    #TODO: get load fraction
    #TODO: specify which attachments carry which loads
    #TODO: calculate highest mass bracket
    #TODO: calc bearing and pullthrough ->new mass
    #TODO: subtract the holes due to the fueltanks

    """
    Here the forces on the transverse panels are calculated and then these are added to the load P 
    for later iterations of the structural cylinder
    """

    att_and_panelMass = Main.CalcMass(closePanelList+transversePanelList, Attachments)
    Panel1Mass = 110 + 0.5 * (Loads.volLarge/Loads.volTot*1085) + (Loads.volSmall/Loads.volTot*1085) + att_and_panelMass/2 #mass on the first transverse panel
    Panel2Mass = 115.9 + 0.5 * (Loads.volLarge/Loads.volTot*1085) + att_and_panelMass/2 #mass on the second transverse panel

    #updates the total load on the structural cylinder
    Loads.totalMass=Loads.initialTotalMass + Panel1Mass + Panel2Mass + structuralCylinder.mass
    Loads.P = Loads.A * Loads.totalMass

    #TODO: update the attachment force and thus their mass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    here the structural cylinder is sized and its mass will also be added to the next iteration
    """

    # Main.hoopStress(structuralCylinder) #gets the thickness by pressure calculation
    #
    # if Main.eulerBuckling(structuralCylinder) < Loads.P[2]/structuralCylinder.calcArea():
    #     print("Fail by Euler Buckling")
    #
    # if Main.shellBuckling(structuralCylinder) < Loads.P[2]/structuralCylinder.calcArea():
    #     print("Fail by Shell Buckling")

    #optimising for buckling (its scuffed)
    Resulto_Buck = optimize.minimize(Main.Buck, [structuralCylinder.t, structuralCylinder.h, structuralCylinder.R, structuralCylinder.half_waves], args=[structuralCylinder.E, structuralCylinder.Poisson, structuralCylinder.SigmaY])
    print(Resulto_Buck) #prints the results of the optimiser
    structuralCylinder.mass = structuralCylinder.rho * Resulto_Buck.fun #the function output volume, so the mass is the output(.fun) times density

    # updates structuralCylinder with the values given by the optimiser
    structuralCylinder.t = Resulto_Buck.x[0]
    structuralCylinder.h = Resulto_Buck.x[1]
    structuralCylinder.R = Resulto_Buck.x[2]
    structuralCylinder.half_waves = Resulto_Buck.x[3]

    #final check just to make sure
    print(f"t = {structuralCylinder.t} m, h = {structuralCylinder.h} m, R = {structuralCylinder.R} m")

    massdiff = structuralCylinder.mass #TODO: add all the mass that is added in the itteration
    break #break to test


