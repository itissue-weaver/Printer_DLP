# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:24 $"

import ttkbootstrap as ttk

from files.constants import font_entry
from templates.AuxiliarFunctions import read_settings, update_settings


def create_input_widgets_display(master):
    settings = read_settings()
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Display")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)
    frame_inputs.configure(style="Custom.TLabelframe")
    # ------------------------parameters display--------------------------
    ttk.Label(frame_inputs, text="Projector dimension [width_cm, height_cm]:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_dimension = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_dimension", [20.0, 20.0])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_dimension, font=font_entry).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_dimension)

    ttk.Label(frame_inputs, text="Projector resolution [width_px, height_px]:", style="Custom.TLabel").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_resolution = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_resolution", [1920, 1080])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_resolution, font=font_entry).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_resolution)

    ttk.Label(frame_inputs, text="Projector offset [x, y, z] normalized:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_offset = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_offset", [0.0, 0.0, 0.0])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_offset, font=font_entry).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_offset)

    ttk.Label(frame_inputs, text="DPI:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_dpi = ttk.StringVar(value=str(settings.get("dpi", "300")))
    ttk.Entry(frame_inputs, textvariable=entry_dpi, font=font_entry).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dpi)

    ttk.Label(frame_inputs, text="Size projection [(x,y)square normalized]:", style="Custom.TLabel").grid(
        row=4, column=0, sticky="w", padx=10, pady=10
    )
    entry_size_projection = ttk.StringVar(value=", ".join([str(settings.get("size_projector_x", 0.1)), str(settings.get("size_projector_y", 0.1))]))
    ttk.Entry(frame_inputs, textvariable=entry_size_projection, font=font_entry).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_size_projection)
    return entries


class DisplayConfig(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=1)
        self.frame_inputs.columnconfigure(0, weight=1)
        self.entries = create_input_widgets_display(self.frame_inputs)

    def on_close(self):
        # Obtener los valores de las entradas
        projector_dimension = [float(i) for i in self.entries[0].get().split(",")]
        projector_resolution = [int(i) for i in self.entries[1].get().split(",")]
        projector_offset = [float(i) for i in self.entries[2].get().split(",")]
        offset_x_screen = projector_offset[0]
        offset_y_screen = projector_offset[1]
        dpi = int(self.entries[3].get())
        size_projection = [float(i) for i in self.entries[4].get().split(", ")]
        update_settings(
            projector_dimension=projector_dimension,
            projector_resolution=projector_resolution,
            projector_offset=projector_offset,
            dpi=dpi,
            offset_x_screen=offset_x_screen,
            offset_y_screen=offset_y_screen,
            size_projector_x=size_projection[0],
            size_projector_y=size_projection[1]
        )


def create_input_widgets_print(master):
    settings = read_settings()
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Printer")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)
    frame_inputs.configure(style="Custom.TLabelframe")
    # ----------------------parameters print--------------------
    ttk.Label(frame_inputs, text="Layer thickness [mm]:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_depth = ttk.StringVar(value=str(settings.get("layer_depth", "0.5")))
    ttk.Entry(frame_inputs, textvariable=entry_layer_depth, font=font_entry).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_layer_depth)
    ttk.Label(frame_inputs, text="Exposure normal layer [s]:", style="Custom.TLabel").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_delta_layer = ttk.StringVar(value=str(settings.get("delta_layer", "0.5")))
    ttk.Entry(frame_inputs, textvariable=entry_delta_layer, font=font_entry).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_delta_layer)
    ttk.Label(frame_inputs, text="Delay steps z [s]:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_delay_steps_z = ttk.StringVar(value=str(settings.get("delay_z", "0.005")))
    ttk.Entry(frame_inputs, textvariable=entry_delay_steps_z, font=font_entry).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_delay_steps_z)
    ttk.Label(frame_inputs, text="Delay steps plate [s]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_delay_steps_plate = ttk.StringVar(value=str(settings.get("delay_n", "0.01")))
    ttk.Entry(frame_inputs, textvariable=entry_delay_steps_plate, font=font_entry).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_delay_steps_plate)
    ttk.Label(frame_inputs, text="# Bottom Layers:", style="Custom.TLabel").grid(row=4, column=0, sticky="w", padx=10, pady=10)
    entry_bottom_layers = ttk.StringVar(value=str(settings.get("b_layers", "1")))
    ttk.Entry(frame_inputs, textvariable=entry_bottom_layers, font=font_entry).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_bottom_layers)
    ttk.Label(frame_inputs, text="Exposure time B. Layers [s]:", style="Custom.TLabel").grid(
        row=5, column=0, sticky="w", padx=10, pady=10
    )
    entry_e_time_b_layers = ttk.StringVar(value=str(settings.get("e_time_b_layers", "40")))
    ttk.Entry(frame_inputs, textvariable=entry_e_time_b_layers, font=font_entry).grid(
        row=5, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_e_time_b_layers)
    ttk.Label(frame_inputs, text="Delay z lift [s]:", style="Custom.TLabel").grid(
        row=6, column=0, sticky="w", padx=10, pady=10
    )
    entry_delay_z_lift = ttk.StringVar(value=str(settings.get("delay_z_lift", "0.01")))
    ttk.Entry(frame_inputs, textvariable=entry_delay_z_lift, font=font_entry).grid(
        row=6, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_delay_z_lift)
    ttk.Label(frame_inputs, text="Lift height [mm]:", style="Custom.TLabel").grid(
        row=7, column=0, sticky="w", padx=10, pady=10
    )
    entry_lift_height = ttk.StringVar(value=str(settings.get("lift_height", "6")))
    ttk.Entry(frame_inputs, textvariable=entry_lift_height, font=font_entry).grid(
        row=7, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_lift_height)
    ttk.Label(frame_inputs, text="Initial delay retract [s]:", style="Custom.TLabel").grid(
        row=8, column=0, sticky="w", padx=10, pady=10
    )
    entry_initial_d_r_ini = ttk.StringVar(value=str(settings.get("delay_retract_init", 0.01)))
    ttk.Entry(frame_inputs, textvariable=entry_initial_d_r_ini, font=font_entry).grid(
        row=8, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_initial_d_r_ini)
    return entries


class PrinterConfig(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=1)
        self.frame_inputs.columnconfigure(0, weight=1)
        self.entries = create_input_widgets_print(self.frame_inputs)

    def on_close(self):
        # Obtener los valores de las entradas
        settings = read_settings()
        layer_depth = float(self.entries[0].get())
        delta_layer = float(self.entries[1].get())
        delay_z = float(self.entries[2].get())
        delay_n = float(self.entries[3].get())
        b_layers = int(self.entries[4].get())
        e_time_b_layers = float(self.entries[5].get())
        delay_z_lift = float(self.entries[6].get())
        lift_height = float(self.entries[7].get())
        delay_retract_init = float(self.entries[8].get())
        max_z_part = settings.get("max_z_part")
        min_z_part = settings.get("min_z_part")
        total_z = max_z_part - min_z_part
        num_layers = int(total_z / layer_depth)
        update_settings(
            layer_depth=layer_depth,
            delta_layer=delta_layer,
            delay_z=delay_z,
            delay_n=delay_n,
            b_layers=b_layers,
            e_time_b_layers=e_time_b_layers,
            delay_z_lift = float(delay_z_lift),
            lift_height=lift_height,
            delay_retract_init=delay_retract_init,
            num_layers=num_layers
        )
