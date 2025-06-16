# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 23:12 $"

import pyslm
import cv2
import numpy as np

from templates.AuxiliarFunctions import update_settings

import trimesh


def read_stl(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    update_settings(filepath=filepath)
    solid_part = pyslm.Part("myFrameGuide")
    solid_part.setGeometry(filepath)
    solid_part.rotation = kwargs.get("rotation",  [0, 0, 0])
    solid_part.translation = kwargs.get("translation", [0, 0, 0])
    solid_part.scale = kwargs.get("scale",  1)
    solid_part.dropToPlatform()
    solid_trimesh_part = trimesh.load_mesh(filepath)
    # Get the bounding box dimensions
    bounding_box = solid_trimesh_part.bounding_box.extents
    width, height, depth = bounding_box
    width = round(width, 3)
    height = round(height, 3)
    depth = round(depth, 3)
    centroide_list = solid_trimesh_part.centroid.tolist()
    centroide = [round(item, 3) for item in centroide_list]
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


def postprocessor_image(path_image, is_final):
    try:
        # Cargar la imagen con transparencia
        imagen = cv2.imread(path_image, cv2.IMREAD_UNCHANGED)

        # Separar los canales
        b, g, r, a = cv2.split(imagen)

        # Aplicar un filtro morfológico en la transparencia para eliminar pequeños poros
        kernel = np.ones((5, 5), np.uint8)  # Tamaño pequeño para preservar detalles grandes
        a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, kernel)  # Cierra pequeños huecos en la transparencia

        # Convertir en blanco puro cualquier área que ya no sea transparente
        mask = a > 0  # Detecta píxeles no transparentes
        b[mask], g[mask], r[mask] = 255, 255, 255  # Cambia a blanco

        # Reunir los canales
        imagen_final = cv2.merge((b, g, r, a))

        # Guardar la imagen manteniendo la transparencia
        cv2.imwrite(path_image, imagen_final)
    except Exception as e:
        print("error al procesar la imagen", e)
        return False
    return True
