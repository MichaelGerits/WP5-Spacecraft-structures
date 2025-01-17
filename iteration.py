import Main
import numpy as np
import PartLib
from PartLib import structuralCylinder
import Loads
import math
from scipy import optimize
from coordinate_conversion import cylindrical_to_cartesian
from pprint import pprint


preliminary_radius = 0.28
preliminary_thickness = round((Loads.p * preliminary_radius)/structuralCylinder.SigmaY, 6)

Mass = [0, Loads.initialTotalMass]
acceleration = Loads.acceleration
importantIndex = 0  # KEEP TRACK OF WHICH ITERATION WE ARE AT
massdiff = abs(Mass[importantIndex % 2] - Mass[(importantIndex-1) % 2])

#allocates the initial lists
#----------------------------------------------------------------------------------------------------------------------------------
closePanelList = [PartLib.ClosingPanel(w=1, h=1.5)] * PartLib.closingpanelAmount
transversePanelList = [PartLib.TransversePanel(), PartLib.TransversePanel(holes=[{"r": 0.2515}]*4)] + [PartLib.TransversePanel(R_struct=0)] #2transverse panels + 1 closing panels
Attachmentsupper = [] #initialise list
Attachmentslower = [] #initialise list
Attachmentsprop = [] #initialise list
angles = np.linspace(0,360,num=PartLib.AttachmentPerPlate) #equally space the attachments

#attachments to the propellant tanks
Attachmentsprop = [PartLib.Attachment()] * 12 #12 brackets on the top panel (carry half the load)

while massdiff >= 0.001:
    print("\n#############################################iteration general######################################\n")
    print(Mass)
    """
    The original Buckling calculations are done assuming that the mass excluding the structural mass is added
    """

    P = acceleration * Mass[(importantIndex -1) % 2]
    print("P=", P)
    
    #get the load fraction to guess initial weight of hinges
    frac = np.linalg.norm(P)/np.linalg.norm(np.array([538.6, 538.6, 1795]))

    #attachments to the structural cylinder
    for i in range(1, PartLib.AttachmentPerPlate, 2): #assign the positions
        Attachmentsupper.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], 0]), mass=frac*0.016)) #lower plate
        Attachmentslower.append(PartLib.Attachment(pos=np.array([structuralCylinder.R, angles[i], PartLib.transversePanelHeight]), mass=frac*0.016)) #upper plate

    #-----------------------------------------------------------------------------------------------------------------------------------

    #TODO: update facts [X]
    #TODO: update mass with new attachments [X?]

    """
    Here the forces on the transverse panels are calculated and then these are added to the load P 
    for later iterations of the structural cylinder
    """

    att_and_panelMass = Main.CalcMass(closePanelList+transversePanelList, Attachmentsupper+Attachmentslower+Attachmentsprop) #calculates th 

    Panel1Mass = 118.21 + (1085/2) + att_and_panelMass/2 #mass on the first transverse panel
    Panel2Mass = 104.3 + (1085/2) + att_and_panelMass/2 #mass on the second transverse panel

    Zload = Main.CalcAttachForces(Panel1Mass, Panel2Mass)
    for attach in Attachmentsprop+Attachmentslower+Attachmentsupper:
        attach.zload = Zload
    #finds the highest loaded attachments and itterates the size of the attachments with it
    attHighest = Main.FindHighestLoadAttch(Attachmentslower+Attachmentsupper+Attachmentsprop)
    t=Main.ItterateAttach(attHighest, Attachmentsprop+Attachmentslower+Attachmentsupper)
    for attach in Attachmentsprop+Attachmentslower+Attachmentsupper:
            attach.t=t
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    here the structural cylinder is sized and its mass will also be added to the next iteration
    """

    #optimising for buckling (its scuffed)
    Resulto_Buck = optimize.minimize(Main.Buck, [structuralCylinder.t], args=[structuralCylinder.E, structuralCylinder.Poisson, structuralCylinder.SigmaY, structuralCylinder.h, P[1], structuralCylinder.R], bounds=optimize.Bounds([Main.constrainer(structuralCylinder, P[1])], [0.1]))
    print(Resulto_Buck) #prints the results of the optimiser
    structuralCylinder.mass = structuralCylinder.rho * Resulto_Buck.fun #the function output volume, so the mass is the output(.fun) times density
    # updates structuralCylinder with the values given by the optimiser
    structuralCylinder.t = Resulto_Buck.x[0]
    # structuralCylinder.R = Resulto_Buck.x[1]
    #final check just to make sure
    print(f"t = {structuralCylinder.t} m, R = {structuralCylinder.R} m, mass = {structuralCylinder.mass} kg, V = {2*math.pi*structuralCylinder.R*1.5*structuralCylinder.t} m^3")

    Mass[importantIndex % 2] = Loads.initialTotalMass + structuralCylinder.mass + Panel1Mass + Panel2Mass #TODO: add all the mass that is added in the itteration
    massdiff = abs(Mass[importantIndex % 2] - Mass[(importantIndex - 1) % 2])
    importantIndex +=1
    print(Mass, "Hi")

print("--------------------------closing-------------------------------")
pprint(vars(closePanelList[0]))
print("----------------------------transverse----------------------------")
pprint(vars(transversePanelList[0]))
pprint(vars(transversePanelList[1]))
print("------------------------------transverseclose-------------------------")
pprint(vars(transversePanelList[2]))
print("------------------------------attach-------------------------")
pprint(vars((Attachmentsprop+Attachmentslower+Attachmentsupper)[0]))
print("------------------------------struct-------------------------")
pprint(vars(structuralCylinder))
