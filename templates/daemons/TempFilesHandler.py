# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 04/mar/2025  at 20:50 $"

import os
import shutil
import threading
import time
import zipfile

from templates.AuxFunctionsPlots import read_stl
from templates.AuxiliarFunctions import read_settings
from templates.GUI.PlotFrame import PlotSTL
from templates.midleware.MD_Printer import send_settings_printer, send_zip_file
from templates.AuxiliarHatcher import build_hatcher


class TempFilesHandler(threading.Thread):
    def __init__(self, directory, zip_name, master_plot, type_c):
        super().__init__()
        self.filepath_zip = directory + "/" + zip_name
        self.directory = directory
        self.type = type_c
        self.master_plot = master_plot
        settings = read_settings()
        self.ploter = PlotSTL(
            self.master_plot,
            layer=None,
            type_plot="layer",
            dpi=settings.get("dpi"),
            save_temp_flag=True,
            path_to_save="",
        )
        if not os.path.exists(directory):
            os.makedirs(directory)

    def run(self):
        match self.type:
            case "compress":
                self.slice_and_compress()
            case "uncompress":
                self.uncompress()
            case _:
                print("Invalid type")

    def slice_and_compress(self):
        settings = read_settings()
        layer_depth = settings.get("layer_depth")
        max_z_part = settings.get("max_z_part")
        min_z_part = settings.get("min_z_part")
        total_z = max_z_part - min_z_part
        num_layers = int(total_z / layer_depth)
        # read the stl file and calculate the layers
        # the geometry is placed(rotate and translate) against the platform XY
        solid_trimesh_part, solid_part = read_stl(
            file_path=settings.get("filepath"),
            rotation=settings.get("rotation"),
            scale=settings.get("scale"),
            translation=settings.get("translation"),
        )
        hatcher_type = settings.get("hatcher_type")
        hatch_angle = settings.get("hatch_angle")
        volume_offset_hatch = settings.get("volume_offset_hatch")
        spot_compensation = settings.get("spot_compensation")
        num_inner_contours = settings.get("num_inner_contours")
        num_outer_contours = settings.get("num_outer_contours")
        hatch_spacing = settings.get("hatch_spacing")
        stripe_width = settings.get("stripe_width")
        my_hatcher = build_hatcher(
            hatcher_type=hatcher_type,
            stripe_width=stripe_width,
            hatch_angle=hatch_angle,
            volume_offset_hatch=volume_offset_hatch,
            spot_compensation=spot_compensation,
            num_inner_contours=num_inner_contours,
            num_outer_contours=num_outer_contours,
            hatch_spacing=hatch_spacing,
        )
        layer_sliced = 1
        with zipfile.ZipFile(self.filepath_zip, "w") as zipf:
            for n_layer in range(1, num_layers):
                current_z = n_layer * layer_depth
                # print(f"current_z: {current_z}")
                geom_slice = solid_part.getVectorSlice(current_z)
                # print("slicing: ", settings.get("filepath"), " at z=", current_z)
                # Perform the hatching operations
                layer = my_hatcher.hatch(geom_slice)
                dpi = settings.get("dpi")
                projector_dimension = settings.get("projector_dimension")
                centroide = settings.get("centroide", [0, 0, 0])
                width = settings.get("width_part", 0.0)
                height = settings.get("height_part", 0.0)
                self.ploter.plotLayer(
                    dpi,
                    layer,
                    projector_dimension[0],
                    projector_dimension[1],
                    f"files/img/temp{n_layer}.png",
                    centroide,
                    width,
                    height,
                    clean_plot=True,
                )
                layer_sliced += 1
                self.update_progress(num_layers, layer_sliced)
                zipf.write(f"files/img/temp{n_layer}.png", f"temp{n_layer}.png")
                if os.path.exists(f"files/img/temp{n_layer}.png"):
                    os.remove(f"files/img/temp{n_layer}.png")
                time.sleep(0.1)
        self.send_settings_and_file()
        return True

    def send_settings_and_file(self):
        code, data = send_settings_printer()
        print("send_settings_printer: ", code, data)
        code, data = send_zip_file(self.filepath_zip)
        print("send_zip_file: ", code, data)

    def update_progress(self, total, actual):
        percentage = (actual / total) * 100.0
        self.master_plot.on_update_progress(round(percentage, 2))

    def uncompress(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
            os.makedirs(f"{self.directory}/extracted")
        else:
            os.makedirs(f"{self.directory}/extracted")
        try:
            # Extrae todos los archivos del archivo ZIP
            with zipfile.ZipFile(self.filepath_zip, "r") as zipf:
                zipf.extractall("files/img/extracted")
            return True
        except Exception as e:
            print("Error al descomprimir el archivo:", e)
            return False
