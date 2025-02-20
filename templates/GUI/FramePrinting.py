# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:18 $"

import os

import ttkbootstrap as ttk

from templates.AuxFunctionsPlots import read_stl
from templates.AuxiliarFunctions import read_settings
from templates.GUI.PlotFrame import PlotSTL


def create_widgets_status(master):
    widgets = []
    status_meter = ttk.Meter(
        master=master,
        metersize=180,
        padding=5,
        amounttotal=100,
        amountused=0,
        subtext="%",
        interactive=False,
        textright="%",
    )
    status_meter.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    widgets.append(status_meter)
    return widgets


def create_widgets_resume(master):
    settings = read_settings()
    widgets = []
    ttk.Label(master, text="File name:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    filepath = settings.get("filepath", "Not filepath")
    entry_file_name = ttk.StringVar(value=os.path.basename(filepath))
    ttk.Entry(master, textvariable=entry_file_name, state="readonly").grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_file_name)
    ttk.Label(master, text="Width <x>[mm]:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entry_width = ttk.StringVar(value=str(settings.get("width_part", "0.0")))
    ttk.Entry(master, textvariable=entry_width, state="readonly").grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_width)
    ttk.Label(master, text="Height <y>[mm]:").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entry_height = ttk.StringVar(value=str(settings.get("height_part", "0.0")))
    ttk.Entry(master, textvariable=entry_height, state="readonly").grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_height)
    ttk.Label(master, text="Depth  <z>[mm]:").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entry_length = ttk.StringVar(value=str(settings.get("length_part", "0.0")))
    ttk.Entry(master, textvariable=entry_length, state="readonly").grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_length)
    delta_layer = settings.get("delta_layer", 0.5)  # seconds
    layers = settings.get("num_layers", 1)
    estimated_time = delta_layer * layers
    hours = int(estimated_time / 3600)
    minutes = int((estimated_time % 3600) / 60)
    seconds = int(estimated_time % 60)
    ttk.Label(master, text="Estimated time:").grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    entry_estimated_time = ttk.StringVar(
        value=f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds"
    )
    ttk.Entry(master, textvariable=entry_estimated_time, state="readonly").grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_estimated_time)
    return widgets


class FramePrinting(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.is_printing = False
        settings = read_settings()
        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_main_info.columnconfigure((0, 1, 2), weight=1)
        self.frame_main_info.rowconfigure(0, weight=1)
        solid_trimesh_part = read_stl(
            file_path=settings.get("filepath", "files/pyramid_test.stl"),
        )
        self.frame_plot = PlotSTL(
            self.frame_main_info, solid_trimesh_part=solid_trimesh_part
        )
        self.frame_plot.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.frame_resume = ttk.Frame(self.frame_main_info)
        self.frame_resume.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.frame_resume.columnconfigure((0, 1), weight=1)
        self.frame_resume.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.resume_widgets = create_widgets_resume(self.frame_resume)

        self.frame_tanks_and_plot = ttk.Frame(self.frame_main_info)
        self.frame_tanks_and_plot.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.frame_tanks_and_plot.columnconfigure(0, weight=1)
        self.frame_tanks_and_plot.rowconfigure((0, 1, 2, 3), weight=1)
        ttk.Label(self.frame_tanks_and_plot, text="Status", font=("Arial", 22)).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.frame_status = ttk.Frame(self.frame_tanks_and_plot)
        self.frame_status.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_status.columnconfigure(0, weight=1)
        self.frame_status.rowconfigure(0, weight=1)
        self.status_widgets = create_widgets_status(self.frame_status)
        ttk.Label(self.frame_tanks_and_plot, text="Materials", font=("Arial", 22)).grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.frame_tanks = SubFrameBars(self.frame_tanks_and_plot)
        self.frame_tanks.columnconfigure(0, weight=1)
        self.frame_tanks.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame_tanks.grid(row=3, column=0, sticky="nsew", padx=15, pady=15)

        # ----------------------Button----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure((0, 1), weight=1)

        ttk.Button(
            self.frame_buttons,
            text="Send settings",
            command=self.send_settings_callback,
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        self.print_button = ttk.Button(
            self.frame_buttons,
            text="Print",
            command=self.print_callback,
            bootstyle="success",
        )
        self.print_button.grid(row=0, column=1, sticky="n", padx=15, pady=15)

    def print_callback(self):
        self.is_printing = not self.is_printing
        if self.is_printing:
            self.print_button.config(text="Stop printing")
            self.print_button.config(bootstyle="danger")
        else:
            self.print_button.config(text="Print")
            self.print_button.config(bootstyle="success")

    def send_settings_callback(self):
        print("Send settings")
        pass


class SubFrameBars(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)

        # ----------------------widgets----------------------
        ttk.Label(self, text="Tank 1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tank1 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.tank1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 2").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.tank2 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.tank2.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 3").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.tank3 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.tank3.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 4").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.tank4 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.tank4.grid(row=7, column=0, sticky="nsew", padx=10, pady=10)
        self.update_levels()

    def update_levels(self):
        settings = read_settings()
        self.tank1.configure(value=settings.get("quantity1", 0.0))
        self.tank2.configure(value=settings.get("quantity2", 0.0))
        self.tank3.configure(value=settings.get("quantity3", 0.0))
        self.tank4.configure(value=settings.get("quantity4", 0.0))
