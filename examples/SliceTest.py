# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:12 $"

import trimesh
from pyslm import hatching as hatching

from templates.AuxFunctionsPlots import read_stl

"""
A simple example showing how to use PySLM for generating slices across a 3D model
"""
import pyslm
import pyslm.visualise
from pyslm import hatching as hatching
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Imports the part and sets the geometry to  an STL file (frameGuide.stl)
solidPart = pyslm.Part('inversePyramid')
solidPart.setGeometry('C:/Users/Weaver4/Downloads/W v1.stl')
# solidtrimesh = trimesh.load('C:/Users/Weaver4/Downloads/W v1.stl')
solidPart.origin[0] = 0.0
solidPart.origin[1] = 0.0
solidPart.scaleFactor = 1.0
solidPart.rotation = [0, 0.0, 0]
solidPart.dropToPlatform()


solidtrimesh = solidPart.geometry
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extrae vértices y caras
vertices = solidtrimesh.vertices
faces = solidtrimesh.faces
mesh = Poly3DCollection(vertices[faces], alpha=0.7, edgecolor='k')
ax.add_collection3d(mesh)

# Ajusta límites
scale = solidtrimesh.bounds.flatten()
ax.auto_scale_xyz(scale, scale, scale)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title("STL Model in Specific Figure and Axes")
plt.tight_layout()
plt.show()

solidPart.origin[0] = 0.0
solidPart.origin[1] = 0.0
solidPart.scaleFactor = 1.0
solidPart.rotation = [0, 0.0, 0]
solidPart.dropToPlatform()

# Create a StripeHatcher object for performing any hatching operations
myHatcher = hatching.Hatcher()

# Set the base hatching parameters which are generated within Hatcher
myHatcher.hatchAngle = 10
myHatcher.volumeOffsetHatch = 0.08
myHatcher.spotCompensation = 0.01
myHatcher.numInnerContours = 2
myHatcher.numOuterContours = 1
myHatcher.hatchSortMethod = hatching.AlternateSort()

# Set the layer thickness
layerThickness = 0.05 # [mm]

# Perform the slicing. Return coords paths should be set so they are formatted internally.
#myHatcher.layerAngleIncrement = 66.7

#Perform the hatching operations
print('Hatching Started')

layers = []

for z in np.arange(0+layerThickness, solidPart.boundingBox[5], layerThickness):

    # Typically the hatch angle is globally rotated per layer by usually 66.7 degrees per layer
    myHatcher.hatchAngle += 66.7
    # Slice the boundary
    geomSlice = solidPart.getVectorSlice(z, simplificationFactor=0.2)
    # Hatch the boundary using myHatcher
    layer = myHatcher.hatch(geomSlice)
    # The layer height is set in integer increment of microns to ensure no rounding error during manufacturing
    layer.z = int(z*1000)
    layers.append(layer)

print('Completed Hatching')

# Plot the layer geometries using matplotlib
# Note: the use of python slices to get the arrays
# pyslm.visualise.plotLayers(layers[0:-1:10])

import matplotlib.pyplot as plt
import numpy as np

from pyslm.visualise import plot

fig = plt.figure()
ax = plt.axes(projection='3d')

num_blocks = 4
total_layers = len(layers)
layers_per_block = total_layers // num_blocks

colors = ['red', 'green', 'blue', 'orange']

for i, layer in enumerate(layers):
    z = float(layer.z) / 1000.0
    block_idx = min(i // layers_per_block, num_blocks - 1)
    color = colors[block_idx]

    # Extraemos hatches como coordenadas
    sampling_rate = 7  # Muestra 1 de cada 5 segmentos

    for hatch_geom in layer.getHatchGeometry():
        coords = np.array(hatch_geom.coords).reshape(-1, 2, 2)
        coords = coords[::sampling_rate]  # Submuestreo

        for seg in coords:
            x = [seg[0][0], seg[1][0]]
            y = [seg[0][1], seg[1][1]]
            ax.plot(x, y, zs=z, zdir='z', color=color, linewidth=0.25)

ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')
ax.view_init(elev=15, azim=0)  # Vista desde arriba
plt.show()

