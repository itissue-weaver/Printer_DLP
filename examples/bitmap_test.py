# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 16:09 $"

import trimesh

"""
A simple reference example showing how to use Trimesh functions to convert vector slices obtained from a part into a
bitmap (binary) image of the current slice at very high resolutions.

This internally uses Trimesh's capability, essentially built on the Pillow library, so much credit goes to there, however,
given it's utility generally in AM, it is a valuable function to show how this can be very quickly and conveniently
generated.

This method is very unlikely to be as fast as a dedicated voxeliser method to generate 3D volumes, but is reasonable
technique to generate a stack of bitmap images for DLP, BJF, Inkjet processes.
"""
#
# import numpy as np
# import pyslm
#
# import matplotlib.pyplot as plt
#
# # Imports the part and sets the geometry to  an STL file (frameGuide.stl)
# solidPart = pyslm.Part("myFrameGuide")
# solidPart.setGeometry("files/meniscus-flat.stl")
#
#
# """
# Transform the part:
# Rotate the part 30 degrees about the Z-Axis - given in degrees
# Translate by an offset of (5,10) and drop to the platform the z=0 Plate boundary
# """
# solidPart.origin = [0.0, 0.0, 0.0]
# solidPart.rotation = np.array([0, 0, 0])
# solidPart.scaleFactor = 1.0
# solidPart.dropToPlatform()
#
# solid_trimesh_part = trimesh.load_mesh("files/meniscus-flat.stl")
# # Get the bounding box dimensions
#
# # Note the resolution units are [mm/px], DPI = [px/inch]
# dpi = 300.0
# resolution = 25.4 / dpi
#
# # Return the Path2D object from Trimesh by setting second argument to False
# slice = solidPart.getTrimeshSlice(1)
#
# # Rasterise and cast to a numpy array
# # The origin is set based on the minium XY bounding box of the part. Depending on the platform the user may
# sliceImage = slice.rasterize(pitch=resolution, origin=solidPart.boundingBox[:2])
# sliceImage = np.array(sliceImage)
#
# # For convenience, the same function above is available directly from the Part class
# slice = solidPart.getBitmapSlice(0.5, resolution)
#
# # Obtener las dimensiones del bounding box
# boundingBox = solid_trimesh_part.bounding_box
# width, height, depth = boundingBox.extents
# # print("Ancho:", width)
# # print("Alto:", height)
# # Configura el DPI y la resolución
# dpi = 300.0
# resolution = 25.4 / dpi
#
# # Obtener el slice y rasterizarlo
# slice = solidPart.getBitmapSlice(1.5, resolution)
#
# # Configura el tamaño de la figura según el bounding box del sólido
# fig = plt.figure(frameon=False)
# # fig.set_size_inches(width / 25.4, height / 25.4)  # Ajusta el tamaño de la figura
#
# ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
# ax.set_axis_off()
# fig.add_axes(ax)
# ax.imshow(slice, cmap="gray", origin="lower")
#
# # Guarda la imagen
# plt.savefig("bitmap_test.png", dpi=300, bbox_inches="tight", pad_inches=0)
# plt.show()
