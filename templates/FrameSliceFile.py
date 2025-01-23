# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:05 $"


import pyslm
import ttkbootstrap as ttk
from pyslm import hatching
import pyslm.visualise

from templates.AuxiliarFunctions import update_settings, read_settings
from templates.PlotFrame import PlotSTL


def create_input_widgets(master, **kwargs):
    entries = []
    ttk.Label(master, text="Rotation[0,0,0]:").grid(row=2, column=0, sticky="w")
    entry_rotation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(master, textvariable=entry_rotation).grid(row=2, column=1, sticky="w")
    entries.append(entry_rotation)
    ttk.Label(master, text="Scale[1, 1, 1]:").grid(row=3, column=0, sticky="w")
    entry_scale = ttk.StringVar(value="1.0, 1.0, 1.0")
    ttk.Entry(master, textvariable=entry_scale).grid(row=3, column=1, sticky="w")
    entries.append(entry_scale)
    ttk.Label(master, text="Translation[0, 0, 0]:").grid(row=4, column=0, sticky="w")
    entry_translation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(master, textvariable=entry_translation).grid(row=4, column=1, sticky="w")
    entries.append(entry_translation)
    ttk.Label(master, text="z:").grid(row=5, column=0, sticky="w")
    entry_z = ttk.StringVar(value="0.0")
    ttk.Entry(master, textvariable=entry_z).grid(row=5, column=1, sticky="w")
    entries.append(entry_z)
    ttk.Scale(
        master,
        from_=0.0,
        to=100.0,
        orient="horizontal",
        command=kwargs.get("callback_scale"),
    ).grid(row=5, column=2, sticky="ew")
    return entries


def create_buttons(master, **kwargs):
    ttk.Button(
        master, text="Slice", command=kwargs.get("callback_sliceFile", None)
    ).grid(row=0, column=0, sticky="n")


def read_stl(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    rotation = kwargs.get("rotation", [0, 0, 0])
    scale = kwargs.get("scale", [1, 1, 1])
    translation = kwargs.get("translation", [0, 0, 0])
    update_settings(rotation=rotation, scale=scale, translation=translation)
    solid_part = pyslm.Part("myFrameGuide")
    solid_part.setGeometry(kwargs.get("file_path", None))
    solid_part.rotation = rotation
    solid_part.translation = translation
    solid_part.scale = scale
    solid_part.dropToPlatform()
    return solid_part


class SliceFile(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.entry_z = None
        self.z_value = 0.0
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew")
        self.frame_inputs.columnconfigure(2, weight=1)
        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_scale=lambda value: self.scale_callback(value),
        )
        self.entry_z = self.entries[3]
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew")
        self.frame_buttons.columnconfigure(0, weight=1)
        create_buttons(
            self.frame_buttons,
            callback_sliceFile=self.slice_geometry,
        )
        # ----------------------axes---------------------------
        self.frame_axes = ttk.Frame(self)
        self.frame_axes.grid(row=2, column=0, sticky="nsew")

    def scale_callback(self, value):
        value = float(value)
        if self.z_value != value:
            self.z_value = round(value, 3)
            self.entry_z.set(str(self.z_value))
            self.slice_geometry()

    def slice_geometry(self):
        try:
            settings = read_settings()
            solid_part = read_stl(
                file_path=settings.get("filepath"),
                rotation=[float(x) for x in self.entries[0].get().split(", ")],
                scale=[float(x) for x in self.entries[1].get().split(", ")],
                translation=[float(x) for x in self.entries[2].get().split(", ")],
            )
            print(solid_part.geometry)
            z = float(self.entries[3].get())
            print("slicing: ", settings.get("filepath"), " at z=", z)
            # Create a StripeHatcher object for performing any hatching operations
            my_hatcher = hatching.StripeHatcher()
            my_hatcher.stripeWidth = 5.0  # [mm]

            # Set the base hatching parameters which are generated within Hatcher
            my_hatcher.hatchAngle = 0.0  # [°]
            my_hatcher.volumeOffsetHatch = 0.08  # [mm]
            my_hatcher.spotCompensation = 0.06  # [mm]
            my_hatcher.numInnerContours = 2
            my_hatcher.numOuterContours = 1

            # Slice the object at Z and get the boundaries
            geom_slice = solid_part.getVectorSlice(z)

            # Perform the hatching operations
            layer = my_hatcher.hatch(geom_slice)
            self.frame_axes.destroy()
            self.frame_axes = PlotSTL(self, layer=layer, type_plot="layer")
            self.frame_axes.grid(row=2, column=0, sticky="nsew")
            return layer
        except Exception as e:
            print(e)
            return None
