import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian


preliminary_radius = 0.28
preliminary_thickness = round((Loads.p * preliminary_radius)/structuralCylinder.SigmaY, 6)

massdiff = 10
while massdiff >= 1:
    """
    The original Buckling calculations are done assuming that the mass excluding the structural mass is added
    """

    #allocates the initial lists
    #----------------------------------------------------------------------------------------------------------------------------------
    closePanelList = [PartLib.ClosingPanel(w=1, h=1.5)] * PartLib.closingpanelAmount
    transversePanelList = [PartLib.TransversePanel(), PartLib.TransversePanel([{"r": 0.2682}]*4)] + [PartLib.TransversePanel(R_struct=0)] #2transverse panels + 1 closing panels
    Attachmentsupper = [] #initialise list
    Attachmentslower = [] #initialise list
    Attachmentsprop = [] #initialise list
    Attachmentshelium = [] #initialise list
    angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

    #get the load fraction to guess initial weight of hinges
    frac = np.linalg.norm(Loads.P)/np.linalg.norm(np.array([538.6, 538.6, 1795]))

    #attachments to the propellant tanks
    Attachmentsprop = [PartLib.Attachment()] * 12
    Attachmentsprop = [PartLib.Attachment()] * 3
    #attachments to the structural cylinder
    for i in range(1, PartLib.AttachmentPerPlate, 2): #assign the positions
        Attachmentsupper.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]), mass=frac*0.016)) #lower plate
        Attachmentslower.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]), mass=frac*0.016)) #upper plate

    #TODO: add attachments for the fueltanks (for both the prop tanks and helium) + loads
    #-----------------------------------------------------------------------------------------------------------------------------------

    #TODO: specify which attachments carry which loads []
    #TODO: update facts []
    #TODO: update mass with new attachments

    """
    Here the forces on the transverse panels are calculated and then these are added to the load P 
    for later iterations of the structural cylinder
    """

    att_and_panelMass = Main.CalcMass(closePanelList+transversePanelList, Attachmentsupper+Attachmentslower+Attachmentshelium+Attachmentsprop) #calculates th 

    Panel1Mass = 118.21 + (1085/2) +  att_and_panelMass/2 #mass on the first transverse panel
    Panel2Mass = 104.3 + (1085/2) + att_and_panelMass/2 #mass on the second transverse panel


    #updates the total load on the structural cylinder
    Loads.totalMass=Loads.initialTotalMass + Panel1Mass + Panel2Mass + structuralCylinder.mass
    Loads.P = Loads.A * Loads.totalMass

    #TODO: updates the loads on the cylinder attachment

    att = Main.FindHighestLoadAttch(Attachmentslower+Attachmentsupper+Attachmentshelium+Attachmentsprop)
    Main.ItterateAttach(att, Attachmentslower+Attachmentsupper+Attachmentshelium+Attachmentsprop)#update the attachment force and thus their mass

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
    Resulto_Buck = optimize.minimize(Main.Buck, [structuralCylinder.t, structuralCylinder.R], args=[structuralCylinder.E, structuralCylinder.Poisson, structuralCylinder.SigmaY, structuralCylinder.h], bounds=optimize.Bounds([preliminary_thickness, 0.001], [0.1, 0.28]))
    print(Resulto_Buck) #prints the results of the optimiser
    structuralCylinder.mass = structuralCylinder.rho * Resulto_Buck.fun #the function output volume, so the mass is the output(.fun) times density
    # updates structuralCylinder with the values given by the optimiser
    structuralCylinder.t = Resulto_Buck.x[0]
    structuralCylinder.R = Resulto_Buck.x[1]
    #final check just to make sure
    print(f"t = {structuralCylinder.t} m, R = {structuralCylinder.R} m", 2*math.pi*structuralCylinder.R*1.5*structuralCylinder.t, "m^3")

    massdiff = structuralCylinder.mass #TODO: add all the mass that is added in the itteration


