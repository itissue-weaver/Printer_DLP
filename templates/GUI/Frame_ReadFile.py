# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 19:25 $"

from tkinter import filedialog

import ttkbootstrap as ttk

from templates.AuxFunctionsPlots import read_stl
from templates.GUI.PlotFrame import PlotSTL


def create_input_widgets(master, **kwargs):
    entries = []
    ttk.Label(master, text="Path: ").grid(row=0, column=1, sticky="w", padx=3, pady=5)
    entry_path = kwargs.get("var_path")
    ttk.Label(master, textvariable=entry_path).grid(
        row=0, column=2, sticky="ew", padx=3, pady=5
    )
    entries.append(entry_path)
    ttk.Button(
        master, text="Buscar archivo", command=kwargs.get("callback_searchFile", None)
    ).grid(row=0, column=0, sticky="ew", padx=3, pady=5)
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
        master,
        text="Establecer Geometria",
        command=kwargs.get("callback_setGeometry", None),
    ).grid(row=0, column=0, sticky="n")


class ReadFile(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.file_path = ttk.StringVar()
        self.Figure = None
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.LabelFrame(self, text="3D")
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(2, weight=1)
        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_searchFile=lambda: import_file_stl(self.file_path),
            var_path=self.file_path,
        )
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew")
        self.frame_buttons.columnconfigure(0, weight=1)
        create_buttons(
            self.frame_buttons,
            callback_setGeometry=self.set_geometry_from_file,
        )
        # ----------------------axes---------------------------
        self.frame_axes = ttk.Frame(self)
        self.frame_axes.grid(row=2, column=0, sticky="nsew")

    def set_geometry_from_file(self):
        # try:
        filepath = self.file_path.get()
        if filepath == "":
            print("No file selected")
            return None
        solid_trimesh_part, solid_part = read_stl(
            file_path=filepath,
        )
        self.frame_axes.destroy()
        self.frame_axes = PlotSTL(self, solid_trimesh_part=solid_trimesh_part)
        self.frame_axes.grid(row=2, column=0, sticky="nsew")
        return solid_trimesh_part
        # except Exception as e:
        #     print("error setting geometry:", e)
        #     return None
