# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 15:24 $"

import numpy as np
import trimesh
from pyslm import hatching


def build_hatcher(
    hatcher_type,
    hatch_angle,
    volume_offset_hatch,
    spot_compensation,
    num_inner_contours,
    num_outer_contours,
    hatch_spacing,
    stripe_width,
):
    # Create a StripeHatcher object for performing any hatching operations
    match hatcher_type:
        case "Base":
            my_hatcher = hatching.Hatcher()
        case "Island":
            my_hatcher = hatching.IslandHatcher()
        case "Stripe":
            my_hatcher = hatching.StripeHatcher()
        case _:
            my_hatcher = hatching.StripeHatcher()
    my_hatcher.stripeWidth = stripe_width
    my_hatcher.hatchAngle = hatch_angle
    my_hatcher.volumeOffsetHatch = volume_offset_hatch
    my_hatcher.spotCompensation = spot_compensation
    my_hatcher.numInnerContours = num_inner_contours
    my_hatcher.numOuterContours = num_outer_contours
    my_hatcher.hatchSpacing = hatch_spacing
    return my_hatcher


def divide_solid_in_z_parts(solid_trimesh_part, parts):
    z_min, z_max = solid_trimesh_part.bounds[0][2], solid_trimesh_part.bounds[1][2]
    z_step = (z_max - z_min) / parts
    sub_solids = []

    for i in range(parts):
        z_lower = z_min + i * z_step
        z_upper = z_min + (i + 1) * z_step

        mask = (solid_trimesh_part.vertices[:, 2] >= z_lower) & (
            solid_trimesh_part.vertices[:, 2] < z_upper
        )

        # Filtrar vértices y obtener sus índices
        sub_vertices = solid_trimesh_part.vertices[mask]
        vertex_indices = np.where(mask)[0]

        # Crear un diccionario para mapear los índices originales a los nuevos índices
        index_mapping = {
            old_index: new_index for new_index, old_index in enumerate(vertex_indices)
        }

        # Filtrar y mapear caras
        sub_faces = []
        for face in solid_trimesh_part.faces:
            if all(index in index_mapping for index in face):
                sub_faces.append([index_mapping[index] for index in face])

        subsolid = trimesh.Trimesh(vertices=sub_vertices, faces=np.array(sub_faces))
        sub_solids.append(subsolid)

    return sub_solids