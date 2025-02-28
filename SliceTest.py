# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:12 $"

import trimesh
from pyslm import hatching as hatching

from templates.AuxFunctionsPlots import read_stl


def read_stl_trimesh(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    trimesh_part = trimesh.load_mesh(filepath)
    return trimesh_part


if __name__ == "__main__":
    # Imports the part and sets the geometry to an STL file (frameGuide.stl)
    # solidPart = pyslm.Part("myFrameGuide")
    # solidPart.setGeometry("files/pyramid_test.stl")
    solid_trimesh_part, solidPart = read_stl(file_path="files/meniscus-flat.stl")
    # solidPart.rotation = [0, 0, 0]
    # solidPart.translation = [0, 0, 0]
    # solidPart.scale = [1, 1, 1]
    # solidPart.dropToPlatform()
    bounding_box = solid_trimesh_part.bounding_box.extents
    width, height, depth = bounding_box
    print(width, height, depth)
    other_bouded_box = solidPart.boundingBox
    print("other: ", other_bouded_box)
    min_x, min_y, min_z, max_x, max_y, max_z = other_bouded_box
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    print(width, height, depth)
