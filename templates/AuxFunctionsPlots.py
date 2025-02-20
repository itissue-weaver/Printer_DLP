# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 23:12 $"

from templates.AuxiliarFunctions import update_settings

import trimesh


def read_stl(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    update_settings(filepath=filepath)
    solid_trimesh_part = trimesh.load_mesh(filepath)
    # Get the bounding box dimensions
    bounding_box = solid_trimesh_part.bounding_box.extents
    width, height, depth = bounding_box
    width = round(width, 3)
    height = round(height, 3)
    depth = round(depth, 3)
    centroide = solid_trimesh_part.centroid.tolist()
    update_settings(
        filepath=filepath,
        width_part=width,
        height_part=height,
        depth_part=depth,
        centroide=centroide,
    )
    return solid_trimesh_part
