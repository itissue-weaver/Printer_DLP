# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 23:12 $"

import pyslm

from templates.AuxiliarFunctions import update_settings

import trimesh


def read_stl(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    update_settings(filepath=filepath)
    solid_part = pyslm.Part("myFrameGuide")
    solid_part.setGeometry(filepath)
    solid_part.rotation = kwargs.get("rotation")
    solid_part.translation = kwargs.get("translation")
    solid_part.scale = kwargs.get("scale")
    solid_part.dropToPlatform()
    solid_trimesh_part = trimesh.load_mesh(filepath)
    # Get the bounding box dimensions
    bounding_box = solid_trimesh_part.bounding_box.extents
    width, height, depth = bounding_box
    width = round(width, 3)
    height = round(height, 3)
    depth = round(depth, 3)
    centroide = solid_trimesh_part.centroid.tolist()
    min_x, min_y, min_z, max_x, max_y, max_z = solid_part.boundingBox
    # print("save: ", solid_part.boundingBox)
    update_settings(
        filepath=filepath,
        width_part=width,
        height_part=height,
        depth_part=depth,
        centroide=centroide,
        min_x_part=min_x,
        min_y_part=min_y,
        min_z_part=min_z,
        max_x_part=max_x,
        max_y_part=max_y,
        max_z_part=max_z,
    )
    return solid_trimesh_part, solid_part
