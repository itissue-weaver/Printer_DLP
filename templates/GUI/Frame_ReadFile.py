# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 19:25 $"

from tkinter import filedialog

import ttkbootstrap as ttk

from templates.AuxFunctionsPlots import read_stl
from templates.AuxiliarFunctions import read_settings, update_settings
from templates.GUI.PlotFrame import PlotSTL


def create_input_widgets(master, **kwargs):
    entries = []
    ttk.Label(master, text="Path: ", style="Custom.TLabel").grid(
        row=0, column=1, sticky="w", padx=3, pady=5
    )
    entry_path = kwargs.get("var_path")
    ttk.Label(master, textvariable=entry_path, style="Custom.TLabel").grid(
        row=0, column=2, sticky="ew", padx=3, pady=5
    )
    entries.append(entry_path)
    ttk.Button(
        master,
        text="Buscar archivo",
        command=kwargs.get("callback_searchFile", None),
        style="primary.TButton",
    ).grid(row=0, column=0, sticky="ew", padx=3, pady=5)
    return entries


def import_file_stl(var_path, var_path_show):
    filepath = filedialog.askopenfilename(
        title="Select a file", filetypes=[("STL files", "*.stl")]
    )
    if filepath:
        print("Selected file:", filepath)
        var_path.set(value=filepath)
        var_path_show.set(value=filepath.split("/")[-1])
    else:
        print("No file selected")
        var_path.set(value="")
        var_path_show.set(value="")


def create_buttons(master, **kwargs):
    ttk.Button(
        master,
        text="Establecer Geometria",
        command=kwargs.get("callback_setGeometry", None),
        style="Custom.TButton",
    ).grid(row=0, column=0, sticky="n")


class ReadFile(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.callbacks = kwargs.get("callbacks", {})
        self.columnconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.file_path = ttk.StringVar()
        self.file_path_show =  ttk.StringVar()
        self.Figure = None
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.LabelFrame(self, text="3D")
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(2, weight=1)
        self.frame_inputs.configure(style="Custom.TLabelframe")
        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_searchFile=lambda: import_file_stl(self.file_path, self.file_path_show),
            var_path=self.file_path_show,
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

    def set_geometry_from_file(self, is_init=False):
        settings = read_settings()
        status_frames = settings.get("status_frames", [0, 0, 0, 0])
        solid_trimesh_part = None
        flag_error = False
        try:
            filepath = self.file_path.get() if  not is_init else settings.get("filepath")
            self.file_path_show.set(value=filepath.split("/")[-1])
            if filepath == "":
                print("No file selected set geometry button")
                return None
            rotation = settings.get("rotation")
            scale = settings.get("scale")
            translation = settings.get("translation")
            solid_trimesh_part, solid_part = read_stl(
                file_path=filepath,
                rotation=rotation,
                scale=scale,
                translation=translation
            )
            self.frame_axes.destroy()
            self.frame_axes = PlotSTL(self, solid_trimesh_part=solid_trimesh_part, solid_part=solid_part)
            self.frame_axes.grid(row=2, column=0, sticky="nsew")
            status_frames[1] = 1
        except Exception as e:
            print("error setting geometry in frame read file:", e)
            status_frames[1] = 0
            flag_error = True
        self.callbacks["change_tab_text"](status_frames, "from read file")
        update_settings(status_frames=status_frames)
        if not is_init:
            self.callbacks["on_geometry_changed"]()
        return solid_trimesh_part

    def init_frame_from_settings(self):
        settings = read_settings()
        filepath = settings.get("filepath", "")
        self.file_path.set(value=filepath)
        self.file_path_show.set(value=filepath.split("/")[-1])
        self.set_geometry_from_file()