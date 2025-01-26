# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:05 $"

import threading

import pyslm
import ttkbootstrap as ttk
from pyslm import hatching
import pyslm.visualise

from templates.AuxiliarFunctions import update_settings, read_settings
from templates.DLPViewer import DlpViewer
from templates.PlotFrame import PlotSTL

from tkinter import messagebox


def create_input_widgets(master, **kwargs):
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Parameters")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure((0, 1), weight=1)
    frame_geometry = ttk.LabelFrame(frame_inputs, text="Geometry")
    frame_geometry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_geometry.columnconfigure(1, weight=1)
    ttk.Label(frame_geometry, text="File:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Label(frame_geometry, textvariable=kwargs.get("var_path")).grid(
        row=0, column=1, sticky="ew", columnspan=2, padx=5, pady=5
    )
    ttk.Label(frame_geometry, text="Rotation[x,y,z]:").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entry_rotation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(frame_geometry, textvariable=entry_rotation).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_rotation)
    ttk.Label(frame_geometry, text="Scale[x,y,z]:").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entry_scale = ttk.StringVar(value="1.0, 1.0, 1.0")
    ttk.Entry(frame_geometry, textvariable=entry_scale).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_scale)
    ttk.Label(frame_geometry, text="Translation[x,y,z]:").grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    entry_translation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(frame_geometry, textvariable=entry_translation).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_translation)

    frame_hatching = ttk.LabelFrame(frame_inputs, text="Hatching")
    frame_hatching.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    frame_hatching.columnconfigure(1, weight=1)
    ttk.Label(frame_hatching, text="Hatcher type:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatcher_type = ttk.StringVar(value="Base")
    ttk.Combobox(
        frame_hatching,
        values=["Base", "Island", "Stripe"],
        textvariable=entry_hatcher_type,
        state="readonly",
    ).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_hatcher_type)
    ttk.Label(frame_hatching, text="Hatch angle [º]:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatch_angle = ttk.StringVar(value="10.0")
    ttk.Entry(frame_hatching, textvariable=entry_hatch_angle).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_hatch_angle)
    ttk.Label(frame_hatching, text="Volume offset hatch [mm]:").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_volume_offset = ttk.StringVar(value="0.0")
    ttk.Entry(frame_hatching, textvariable=entry_volume_offset).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_volume_offset)
    ttk.Label(frame_hatching, text="Spot compensation [mm]:").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_spot_compensation = ttk.StringVar(value="0.0")
    ttk.Entry(frame_hatching, textvariable=entry_spot_compensation).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_spot_compensation)
    ttk.Label(frame_hatching, text="Inner contours:").grid(
        row=4, column=0, sticky="w", padx=10, pady=10
    )
    entry_inner_contours = ttk.StringVar(value="2")
    ttk.Entry(frame_hatching, textvariable=entry_inner_contours).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_inner_contours)
    ttk.Label(frame_hatching, text="Outer contours:").grid(
        row=5, column=0, sticky="w", padx=10, pady=10
    )
    entry_outer_contours = ttk.StringVar(value="1")
    ttk.Entry(frame_hatching, textvariable=entry_outer_contours).grid(
        row=5, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_outer_contours)
    ttk.Label(frame_hatching, text="Hatch spacing [mm]:").grid(
        row=6, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatch_spacing = ttk.StringVar(value="0.5")
    ttk.Entry(frame_hatching, textvariable=entry_hatch_spacing).grid(
        row=6, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_hatch_spacing)
    ttk.Label(frame_hatching, text="Stripe width [mm]:").grid(
        row=7, column=0, sticky="w", padx=10, pady=10
    )
    entry_stripe_width = ttk.StringVar(value="0.5")
    ttk.Entry(frame_hatching, textvariable=entry_stripe_width).grid(
        row=7, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_stripe_width)
    # ------------------------parameters display--------------------------
    frame_display = ttk.LabelFrame(frame_inputs, text="Display")
    frame_display.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    ttk.Label(frame_display, text="Projector dimension [width_cm, heigth_cm]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_dimension = ttk.StringVar(value="30.0, 20.0")
    ttk.Entry(frame_display, textvariable=entry_projector_dimension).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_dimension)
    ttk.Label(frame_display, text="Projector resolution [width_px, heigth_px]:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_resolution = ttk.StringVar(value="1920, 1080")
    ttk.Entry(frame_display, textvariable=entry_projector_resolution).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_resolution)
    ttk.Label(frame_display, text="Projector offset [x, y, z] cm:").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_offset = ttk.StringVar(value="0.0, 0.0, 10.0")
    ttk.Entry(frame_display, textvariable=entry_projector_offset).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_offset)
    ttk.Label(frame_display, text="DPI:").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_dpi = ttk.StringVar(value="300")
    ttk.Entry(frame_display, textvariable=entry_dpi).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dpi)
    # ----------------------parameters visual--------------------
    frame_visual = ttk.LabelFrame(master, text="Visualization")
    frame_visual.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_visual.columnconfigure(2, weight=1)
    ttk.Label(frame_visual, text="z:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_z = ttk.StringVar(value="0.0")
    ttk.Entry(frame_visual, textvariable=entry_z).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_z)
    ttk.Scale(
        frame_visual,
        from_=0.0,
        to=kwargs.get("max_z", 100),
        orient="horizontal",
        command=kwargs.get("callback_scale"),
        variable=entry_z,
    ).grid(row=0, column=2, sticky="ew", padx=15, pady=5)
    return entries


def create_buttons(master, **kwargs):
    ttk.Button(
        master, text="Slice", command=kwargs.get("callback_sliceFile", None)
    ).grid(row=0, column=0, sticky="n")
    ttk.Button(
        master, text="Print", command=kwargs.get("callback_printFile", None)
    ).grid(row=0, column=1, sticky="n")


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

        self.display_thread = None
        self.columnconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.entry_z = None
        self.frame_plot = None
        settings = read_settings()
        filepath = settings.get("filepath")
        self.z_value = 0.0
        self.show_path = ttk.StringVar(
            value=filepath if filepath is not None else "No file selected"
        )
        self.z_max = settings.get("depth_part", 100)
        self.viewer = DlpViewer()
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(0, weight=1)
        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_scale=lambda value: self.scale_callback(value),
            var_path=self.show_path,
            max_z=self.z_max,
        )
        self.entry_z = self.entries[-1]
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew")
        self.frame_buttons.columnconfigure(0, weight=1)
        create_buttons(
            self.frame_buttons,
            callback_sliceFile=self.slice_geometry,
            callback_printFile=self.print_file_callback,
        )
        # ----------------------axes---------------------------
        self.frame_axes = ttk.LabelFrame(self, text="Preview")

        self.frame_axes.columnconfigure(0, weight=1)
        self.frame_axes.rowconfigure(0, weight=1)

    def print_file_callback(self):
        if self.display_thread is not None:
            # kill the thread
            self.display_thread.join()
        self.slice_geometry(save_temp_flag=True)
        self.display_thread = threading.Thread(target=self.viewer.display_image)
        self.display_thread.start()

    def scale_callback(self, value):
        value = float(value)
        if self.z_value != value:
            self.z_value = round(value, 3)
            self.entry_z.set(str(self.z_value))
            self.slice_geometry()

    def slice_geometry(self, save_temp_flag=False):
        try:
            settings = read_settings()
            solid_part = read_stl(
                file_path=settings.get("filepath"),
                rotation=[float(x) for x in self.entries[0].get().split(", ")],
                scale=[float(x) for x in self.entries[1].get().split(", ")],
                translation=[float(x) for x in self.entries[2].get().split(", ")],
            )
            if solid_part is None:
                return None
            update_settings(
                hatcher_type=self.entries[3].get(),
                hatch_angle=float(self.entries[4].get()),
                volume_offset_hatch=float(self.entries[5].get()),
                spot_compensation=float(self.entries[6].get()),
                num_inner_contours=int(self.entries[7].get()),
                num_outer_contours=int(self.entries[8].get()),
                hatch_spacing=float(self.entries[9].get()),
                stripe_width=float(self.entries[10].get()),
            )
            z = float(self.entries[-1].get())
            if not (0 < z < self.z_max):
                msg = "z value out of range"
                messagebox.showerror("Error", msg)
                return None
            print("slicing: ", settings.get("filepath"), " at z=", z)
            # Create a StripeHatcher object for performing any hatching operations
            match self.entries[3].get():
                case "Base":
                    my_hatcher = hatching.Hatcher()
                case "Island":
                    my_hatcher = hatching.IslandHatcher()
                case "Stripe":
                    my_hatcher = hatching.StripeHatcher()
                case _:
                    my_hatcher = hatching.StripeHatcher()
            my_hatcher.stripeWidth = float(self.entries[10].get())
            my_hatcher.hatchAngle = float(self.entries[4].get())  # [deg]
            my_hatcher.volumeOffsetHatch = float(self.entries[5].get())  # [mm]
            my_hatcher.spotCompensation = float(self.entries[6].get())  # [mm]
            my_hatcher.numInnerContours = int(self.entries[7].get())
            my_hatcher.numOuterContours = int(self.entries[8].get())
            # Slice the object at Z and get the boundaries
            geom_slice = solid_part.getVectorSlice(z)
            # Perform the hatching operations
            layer = my_hatcher.hatch(geom_slice)
            self.frame_axes.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
            self.frame_plot.destroy() if self.frame_plot else None
            self.frame_plot = PlotSTL(
                self.frame_axes,
                layer=layer,
                type_plot="layer",
                dpi=300,
                save_temp_flag=save_temp_flag,
            )
            self.frame_plot.grid(row=0, column=0, sticky="nsew")
            return layer
        except Exception as e:
            print(e)
            return None
