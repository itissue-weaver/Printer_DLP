# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:12 $"

import pyslm.visualise
from pyslm import hatching as hatching
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Imports the part and sets the geometry to an STL file (frameGuide.stl)
    solidPart = pyslm.Part("myFrameGuide")
    solidPart.setGeometry("pyramid_test.stl")
    solidPart.rotation = [0, 0, 0]
    solidPart.translation = [0, 0, 0]
    solidPart.scale = [1, 1, 1]
    solidPart.dropToPlatform()

    # Set te slice layer position
    z = 2.0

    # Create a trimesh object
    # solidTrimeshPart = trimesh.load_mesh('pyramid_test.stl')
    # solidTrimeshPart.show()

    # Create a StripeHatcher object for performing any hatching operations
    # myHatcher = hatching.StripeHatcher()
    # myHatcher = hatching.Hatcher()
    # myHatcher = hatching.BaseHatcher()
    myHatcher = hatching.IslandHatcher()
    # myHatcher = hatching.BasicIslandHatcher()

    myHatcher.stripeWidth = 5.0  # [mm]

    # Set the base hatching parameters which are generated within Hatcher
    myHatcher.hatchAngle = 0.0  # [°]
    myHatcher.volumeOffsetHatch = (
        0.08  # [mm] Offset between internal and external boundary
    )
    myHatcher.spotCompensation = (
        0.06  # [mm] Additional offset to account for laser spot size
    )
    myHatcher.numInnerContours = 2
    myHatcher.numOuterContours = 1
    myHatcher.hatchSpacing = 0.1  # [mm] The spacing between hatch lines

    # Slice the object at Z and get the boundaries
    geomSlice = solidPart.getVectorSlice(z)

    # Perform the hatching operations
    layer = myHatcher.hatch(geomSlice)

    # Plot the layer geometries generated
    figure, axes = pyslm.visualise.plot(
        layer, plot3D=True, plotOrderLine=True, plotArrows=False
    )
    figure.savefig("pyramid_test.png", dpi=300)
    plt.show()
