# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 19:25 $"

from tkinter import filedialog

import trimesh
import ttkbootstrap as ttk

from templates.AuxiliarFunctions import update_settings
from templates.PlotFrame import PlotSTL


def create_input_widgets(master, **kwargs):
    entries = []
    ttk.Label(master, text="File path:").grid(row=0, column=0, sticky="w")
    entry_path = kwargs.get("var_path")
    ttk.Entry(master, textvariable=entry_path).grid(row=0, column=2, sticky="ew")
    entries.append(entry_path)
    ttk.Button(
        master, text="Buscar archivo", command=kwargs.get("callback_searchFile", None)
    ).grid(row=0, column=1, sticky="ew")
    return entries


def import_file_stl(var_path):
    filepath = filedialog.askopenfilename(
        title="Select a file", filetypes=[("STL files", "*.stl")]
    )
    if filepath:
        print("Selected file:", filepath)
        var_path.set(value=filepath)
    else:
        print("No file selected")
        var_path.set(value="")


def create_buttons(master, **kwargs):
    ttk.Button(
        master, text="Set gemetry", command=kwargs.get("callback_setGeometry", None)
    ).grid(row=0, column=0, sticky="n")
    ttk.Button(
        master, text="Slice", command=kwargs.get("callback_sliceFile", None)
    ).grid(row=0, column=1, sticky="n")


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
    update_settings(
        filepath=filepath, width_part=width, height_part=height, depth_part=depth
    )
    return solid_trimesh_part


class ReadFile(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.file_path = ttk.StringVar()
        self.Figure = None
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew")
        self.frame_inputs.columnconfigure(2, weight=1)
        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_searchFile=lambda: import_file_stl(self.file_path),
            var_path=self.file_path,
        )
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew")
        self.frame_buttons.columnconfigure((0, 1), weight=1)
        create_buttons(
            self.frame_buttons,
            callback_setGeometry=self.set_geometry_from_file,
            callback_sliceFile=lambda: print("Slice file"),
        )
        # ----------------------axes---------------------------
        self.frame_axes = ttk.Frame(self)
        self.frame_axes.grid(row=2, column=0, sticky="nsew")

    def set_geometry_from_file(self):
        try:
            filepath = self.file_path.get()
            if filepath == "":
                print("No file selected")
                return None
            solid_trimesh_part = read_stl(
                file_path=filepath,
            )
            self.frame_axes.destroy()
            self.frame_axes = PlotSTL(self, solid_trimesh_part=solid_trimesh_part)
            self.frame_axes.grid(row=2, column=0, sticky="nsew")
            return solid_trimesh_part
        except Exception as e:
            print("error setting geometry:", e)
            return None
