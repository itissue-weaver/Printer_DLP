# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:18 $"

import os
import threading
import time

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from files.constants import zip_file_name
from templates.AuxFunctionsPlots import read_stl
from templates.AuxiliarFunctions import read_settings, update_settings
from templates.GUI.PlotFrame import SolidViewer
from templates.GUI.SubFramePrinting import FramePrintingProcess
from templates.daemons.TempFilesHandler import TempFilesHandler


def create_widgets_status(master):
    widgets = []
    status_meter = ttk.Meter(
        master=master,
        metersize=180,
        padding=5,
        amounttotal=100,
        amountused=0,
        subtext="Progress",
        interactive=False,
        textright="%",
    )
    status_meter.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    widgets.append(status_meter)
    return widgets


def create_widgets_resume(master):
    settings = read_settings()
    widgets = []
    ttk.Label(master, text="File name:", font=("Arial", 16, "bold")).grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    filepath = settings.get("filepath", "Not filepath")
    entry_file_name = ttk.StringVar(value=os.path.basename(filepath))
    ttk.Entry(master, textvariable=entry_file_name, state="readonly").grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_file_name)
    ttk.Label(master, text="Width <x>[mm]:", font=("Arial", 16, "bold")).grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entry_width = ttk.StringVar(value=str(settings.get("width_part", "0.0")))
    ttk.Entry(master, textvariable=entry_width, state="readonly").grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_width)
    ttk.Label(master, text="Height <y>[mm]:", font=("Arial", 16, "bold")).grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entry_height = ttk.StringVar(value=str(settings.get("height_part", "0.0")))
    ttk.Entry(master, textvariable=entry_height, state="readonly").grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_height)
    ttk.Label(master, text="Depth  <z>[mm]:", font=("Arial", 16, "bold")).grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entry_length = ttk.StringVar(value=str(settings.get("depth_part", "0.0")))
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
    ttk.Label(master, text="Estimated time:", font=("Arial", 16, "bold")).grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    entry_estimated_time = ttk.StringVar(
        value=f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds"
    )
    ttk.Entry(master, textvariable=entry_estimated_time, state="readonly").grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    widgets.append(entry_estimated_time)
    # -----------------frame sequence--------------------------------
    sequence = settings.get("sequence", [])
    frame_sequence = ttk.Frame(master)
    frame_sequence.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    frame_sequence.columnconfigure(0, weight=1)
    ttk.Label(frame_sequence, text="Sequence: ", font=("Arial", 16, "bold")).grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    tree = ttk.Treeview(
        frame_sequence,
        columns=("Deposit", "Height Z"),
        show="headings",
        height=4,
        style="info.Treeview",
    )
    tree.heading("Deposit", text="Deposit", anchor="center")
    tree.heading("Height Z", text="Height Z [mm]", anchor="center")
    tree.column("Deposit", width=80, anchor="center")
    tree.column("Height Z", width=80, anchor="center")
    tree.grid(row=1, column=0, sticky="n")
    for step in sequence:
        tree.insert("", "end", values=(step["deposit"], step["height_z"]))
    widgets.append(tree)
    return widgets


def simulate_printing(master):
    settings = read_settings()
    layers = settings.get("num_layers", 1)
    delta_layer = settings.get("delta_layer", 0.5)  # seconds
    for i in range(layers):
        time.sleep(delta_layer)
        progress = (i + 1) / layers * 100
        master.status_widgets[0].configure(amountused=round(progress, 2))
        master.update()
    Messagebox.show_info("Printing completed", "Printing")
    master.is_printing = False
    master.is_settings_sent = False

    master.status_widgets[0].configure(amountused=0)
    master.update()



class FramePrinting(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.callbacks = kwargs.get("callbacks", {})
        self.file_handler = None
        self.plotter = None
        self.thread_sim = None
        self.is_sliced = False
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.is_printing = False
        settings = read_settings()
        self.is_settings_sent = False
        self.is_sending = False
        self.frame_process_print = None
        self.is_process_set = False
        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_main_info.columnconfigure((0, 1, 2), weight=1)
        self.frame_main_info.rowconfigure(0, weight=1)
        try:
            filepath_stl = settings.get("filepath", "files/pyramid_test.stl")
            os.path.exists(filepath_stl)
            solid_trimesh_part, solid_part = read_stl(
                file_path=settings.get("filepath", "files/pyramid_test.stl"),
                scale=settings.get("scale"),
                rotation=settings.get("rotation"),
                traslation=settings.get("traslation"),
            )
            self.frame_plot = SolidViewer(
                self.frame_main_info, solid_trimesh_part=solid_trimesh_part, parts=4
            )
            self.frame_plot.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        except Exception as e:
            self.button_refresh = ttk.Button(
                self.frame_main_info,
                text="Read STL",
                command=self.import_file_stl
            )
            self.button_refresh.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            print(e)
        self.frame_resume = ttk.Frame(self.frame_main_info)
        self.frame_resume.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.frame_resume.columnconfigure((0, 1), weight=1)
        self.frame_resume.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.resume_widgets = create_widgets_resume(self.frame_resume)

        self.frame_tanks_and_plot = ttk.Frame(self.frame_main_info)
        self.frame_tanks_and_plot.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.frame_tanks_and_plot.columnconfigure(0, weight=1)
        self.frame_tanks_and_plot.rowconfigure((0, 1, 2, 3), weight=1)
        ttk.Label(
            self.frame_tanks_and_plot, text="Status", font=("Arial", 22, "bold")
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.frame_status = ttk.Frame(self.frame_tanks_and_plot)
        self.frame_status.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_status.columnconfigure(0, weight=1)
        self.frame_status.rowconfigure(0, weight=1)
        self.status_widgets = create_widgets_status(self.frame_status)
        ttk.Label(
            self.frame_tanks_and_plot, text="Materials", font=("Arial", 22, "bold")
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.frame_tanks = SubFrameBars(self.frame_tanks_and_plot)
        self.frame_tanks.columnconfigure(0, weight=1)
        self.frame_tanks.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame_tanks.grid(row=3, column=0, sticky="nsew", padx=15, pady=15)

        # ----------------------Button----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure((0, 2), weight=1)
        my_style = ttk.Style()
        my_style.configure("success.TButton", font=("Arial", 18))
        my_style.configure("primary.TButton", font=("Arial", 18))
        ttk.Button(
            self.frame_buttons,
            text="Set Printing Process",
            command=self.callback_print_process,
            style="primary.TButton",
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        ttk.Button(
            self.frame_buttons,
            text="Send settings",
            command=self.send_settings_callback,
            style="primary.TButton",
        ).grid(row=0, column=1, sticky="n", padx=15, pady=15)
        self.print_button = ttk.Button(
            self.frame_buttons,
            text="Print",
            command=self.print_callback,
            style="success.TButton",
        )
        self.print_button.grid(row=0, column=2, sticky="n", padx=15, pady=15)
        # ---------------------progress bar --------------------
        self.frame_progress = ttk.Frame(self)
        self.frame_progress.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_progress.columnconfigure((0, 1, 2), weight=1)
        ttk.Label(
            self.frame_progress, text="Progress", font=("Arial", 22, "bold")
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.value_progress = ttk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.frame_progress,
            orient="horizontal",
            length=200,
            variable=self.value_progress,
        )
        self.progress_bar.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.progress_bar["maximum"] = 100
        self.value_progress.set(0)
        self.text_progress = ttk.StringVar(value="0%")
        ttk.Label(
            self.frame_progress,
            textvariable=self.text_progress,
            font=("Arial", 22, "bold"),
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.frame_progress.grid_forget()

    def check_parameter_settings(self, settings=None):
        settings = read_settings() if settings is None else settings
        param_list = [
            "sequence"
        ]
        status_frames = settings.get("status_frames", [0, 0, 0, 0])
        status_frames[2] = 1
        for param in param_list:
            if param not in settings.keys():
                status_frames[2] = 0
                break
        self.callbacks["change_tab_text"](status_frames)
        update_settings(status_frames=status_frames)

    def print_callback(self):
        if not self.is_sliced:
            Messagebox.show_error("Settings not sent", "Error")
            return
        self.is_printing = not self.is_printing
        if self.is_printing:
            self.print_button.config(text="Stop printing")
            self.print_button.config(bootstyle="danger")
            if self.thread_sim is not None:
                self.thread_sim.join()
            self.thread_sim = threading.Thread(target=simulate_printing, args=(self,))
            # self.thread_sim.start()
        else:
            self.print_button.config(text="Print")
            self.print_button.config(bootstyle="success")
            if self.thread_sim is not None:
                self.thread_sim.join()
                self.is_settings_sent = False

    def callback_print_process(self):
        if self.frame_process_print is None:
            self.frame_process_print = FramePrintingProcess(self)

    def on_close_print_process(self):
        self.frame_process_print = None
        settings = read_settings()
        sequence = settings.get("sequence", [])
        self.resume_widgets[-1].delete(*self.resume_widgets[-1].get_children())
        for step in sequence:
            self.resume_widgets[-1].insert(
                "", "end", values=(step["deposit"], step["height_z"])
            )
        status_frames = settings.get("status_frames")
        status_frames[3] = 1
        self.callbacks["change_tab_text"](status_frames)

    def on_update_progress(self, progress):
        if not self.is_sending:
            self.frame_progress.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
            self.is_sending = True
        self.value_progress.set(progress)
        self.text_progress.set(f"{progress}%")
        if progress >= 100:
            self.is_sliced = True
            self.is_sending = False
            self.frame_progress.grid_forget()

    def send_settings_callback(self):
        # ---------------------calculate_layers--------------
        self.is_sliced = False
        settings = read_settings()
        depth_part = settings.get("depth_part")
        layer_depth = settings.get("layer_depth")
        max_z_part = settings.get("max_z_part")
        min_z_part = settings.get("min_z_part")
        if depth_part is None:
            msg = "No depth part found"
            Messagebox.show_error(msg, "Error")
            return None
        total_z = max_z_part - min_z_part
        num_layers = int(total_z / layer_depth)
        update_settings(num_layers=num_layers)
        self.file_handler = TempFilesHandler(
            "files/img", zip_file_name, self, "compress"
        )
        self.file_handler.start()

    def import_file_stl(self):
        settings = read_settings()
        try:
            filepath_stl = settings.get("filepath", "files/pyramid_test.stl")
            os.path.exists(filepath_stl)
            solid_trimesh_part, solid_part = read_stl(
                file_path=settings.get("filepath", "files/pyramid_test.stl"),
                scale=settings.get("scale"),
                rotation=settings.get("rotation"),
                traslation=settings.get("traslation"),
            )
            self.frame_plot = SolidViewer(
                self.frame_main_info, solid_trimesh_part=solid_trimesh_part, parts=4
            )
            self.frame_plot.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            if self.button_refresh is not None:
                self.button_refresh.destroy()
        except Exception as e:
            if self.button_refresh is not None:
                return
            self.button_refresh = ttk.Button(
                self.frame_main_info,
                text="Read STL",
                command=self.import_file_stl
            )
            print(e)


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
