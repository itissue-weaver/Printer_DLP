# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:24 $"

import ttkbootstrap as ttk

from templates.AuxiliarFunctions import read_settings, update_settings


def create_input_widgets_display(master):
    settings = read_settings()
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Display")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)

    # ------------------------parameters display--------------------------
    ttk.Label(frame_inputs, text="Projector dimension [width_cm, height_cm]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_dimension = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_dimension", [30.0, 20.0])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_dimension).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_dimension)

    ttk.Label(frame_inputs, text="Projector resolution [width_px, height_px]:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_resolution = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_resolution", [1920, 1080])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_resolution).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_resolution)

    ttk.Label(frame_inputs, text="Projector offset [x, y, z] cm:").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_projector_offset = ttk.StringVar(
        value=", ".join(
            [str(i) for i in settings.get("projector_offset", [0.0, 0.0, 10.0])]
        )
    )
    ttk.Entry(frame_inputs, textvariable=entry_projector_offset).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_projector_offset)

    ttk.Label(frame_inputs, text="DPI:").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_dpi = ttk.StringVar(value=str(settings.get("dpi", "300")))
    ttk.Entry(frame_inputs, textvariable=entry_dpi).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dpi)

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
        dpi = int(self.entries[3].get())
        update_settings(
            projector_dimension=projector_dimension,
            projector_resolution=projector_resolution,
            projector_offset=projector_offset,
            dpi=dpi,
        )


def create_input_widgets_print(master):
    settings = read_settings()
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Printer")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)
    # ----------------------parameters print--------------------
    ttk.Label(frame_inputs, text="Layer depth [mm]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_depth = ttk.StringVar(value=str(settings.get("layer_depth", "0.5")))
    ttk.Entry(frame_inputs, textvariable=entry_layer_depth).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_layer_depth)
    ttk.Label(frame_inputs, text="Delta layer [s]:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_delta_layer = ttk.StringVar(value=str(settings.get("delta_layer", "0.5")))
    ttk.Entry(frame_inputs, textvariable=entry_delta_layer).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_delta_layer)
    ttk.Label(frame_inputs, text="Plate:").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_plate = ttk.StringVar(value=str(settings.get("plate", "1")))
    ttk.Combobox(
        frame_inputs,
        values=["1", "2", "3", "4"],
        textvariable=entry_plate,
        state="readonly",
    ).grid(row=2, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_plate)
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
        layer_depth = float(self.entries[0].get())
        delta_layer = float(self.entries[1].get())
        plate = int(self.entries[2].get())
        update_settings(
            layer_depth=layer_depth,
            delta_layer=delta_layer,
            plate=plate,
        )
