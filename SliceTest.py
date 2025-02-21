# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:12 $"

import numpy as np
import pyslm.visualise
import trimesh
from matplotlib import pyplot as plt
from pyslm import hatching as hatching


def read_stl_trimesh(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    trimesh_part = trimesh.load_mesh(filepath)
    return trimesh_part


if __name__ == "__main__":
    # Imports the part and sets the geometry to an STL file (frameGuide.stl)
    solidPart = pyslm.Part("myFrameGuide")
    solidPart.setGeometry("files/pyramid_test.stl")
    solid_trimesh_part = read_stl_trimesh(file_path="files/pyramid_test.stl")
    solidPart.rotation = [0, 0, 0]
    solidPart.translation = [0, 0, 0]
    solidPart.scale = [1, 1, 1]
    solidPart.dropToPlatform()

    bounding_box = solid_trimesh_part.bounding_box.extents
    width, height, depth = bounding_box
    # divide z in 4 parts
    group_size = depth / 4
    # Set te slice layer position
    z_delta = 0.5
    current_z = 0.0
    resolution = 1  # The resolution of the bitmap to generate [pixels/length unit]
    # Create a figure to visualize the current layer
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    while current_z < depth - z_delta:
        current_z += z_delta
        # Slice the object at Z and get the boundaries
        planexy = solidPart.getBitmapSlice(
            current_z, resolution
        )  # ndarray true false data
        planexy = planexy.astype(float)

        # Create grid for the layer
        x = np.linspace(-width / 2, width / 2, planexy.shape[1])
        y = np.linspace(-height / 2, height / 2, planexy.shape[0])
        X, Y = np.meshgrid(x, y)
        Z = np.ones_like(X) * current_z

        # Plot the current layer
        ax.plot_surface(
            X, Y, Z, facecolors=plt.cm.gray(planexy), rstride=1, cstride=1, alpha=0.5
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("3D Layer Visualization")
    plt.show()
