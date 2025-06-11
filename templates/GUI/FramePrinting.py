# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:18 $"

import os
import queue
import threading
import time
from time import sleep

import ttkbootstrap as ttk
from PIL import Image
from ttkbootstrap.dialogs import Messagebox

from files.constants import zip_file_name, font_tabs, font_entry
from templates.AuxiliarFunctions import read_settings, update_settings, read_flags
from templates.GUI.SubFramePrinting import FramePrintingProcess
from templates.daemons.constants import response_queue
from templates.midleware.MD_Printer import send_start_print, send_stop_print, send_settings_printer

Image.CUBIC = Image.BICUBIC

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
    ttk.Label(master, text="File name:", font=font_tabs).grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    filepath = settings.get("filepath", "Not filepath")
    entry_file_name = ttk.StringVar(value=os.path.basename(filepath))
    ttk.Entry(master, textvariable=entry_file_name, state="readonly", font=font_entry).grid(
        row=0, column=1, sticky="we", padx=5, pady=5
    )
    widgets.append(entry_file_name)
    ttk.Label(master, text="Width <x>[mm]:", font=font_tabs).grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    entry_width = ttk.StringVar(value=str(settings.get("width_part", "0.0")))
    ttk.Entry(master, textvariable=entry_width, state="readonly", font=font_entry).grid(
        row=1, column=1, sticky="we", padx=5, pady=5
    )
    widgets.append(entry_width)
    ttk.Label(master, text="Height <y>[mm]:", font=font_tabs).grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entry_height = ttk.StringVar(value=str(settings.get("height_part", "0.0")))
    ttk.Entry(master, textvariable=entry_height, state="readonly", font=font_entry).grid(
        row=2, column=1, sticky="we", padx=5, pady=5
    )
    widgets.append(entry_height)
    ttk.Label(master, text="Depth  <z>[mm]:", font=font_tabs).grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entry_length = ttk.StringVar(value=str(settings.get("depth_part", "0.0")))
    ttk.Entry(master, textvariable=entry_length, state="readonly", font=font_entry).grid(
        row=3, column=1, sticky="we", padx=5, pady=5
    )
    widgets.append(entry_length)
    delta_layer = settings.get("delta_layer", 0.5)  # seconds
    layers = settings.get("num_layers", 1)
    estimated_time = delta_layer * layers
    hours = int(estimated_time / 3600)
    minutes = int((estimated_time % 3600) / 60)
    seconds = int(estimated_time % 60)
    ttk.Label(master, text="Estimated time:", font=font_tabs).grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    entry_estimated_time = ttk.StringVar(
        value=f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds"
    )
    ttk.Entry(master, textvariable=entry_estimated_time, state="readonly", font=font_entry).grid(
        row=4, column=1, sticky="we", padx=5, pady=5
    )
    widgets.append(entry_estimated_time)
    # -----------------frame sequence--------------------------------
    sequence = settings.get("sequence", [])
    frame_sequence = ttk.Frame(master)
    frame_sequence.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    frame_sequence.columnconfigure(0, weight=1)
    ttk.Label(frame_sequence, text="Sequence: ", font=font_tabs).grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    tree = ttk.Treeview(
        frame_sequence,
        columns=("Deposit", "Height Z"),
        show="headings",
        height=4,
        style="Custom.Treeview",
    )
    tree.heading("Deposit", text="Deposit", anchor="center")
    tree.heading("Height Z", text="Height Z [mm]", anchor="center")
    tree.column("Deposit", width=80, anchor="center")
    tree.column("Height Z", width=80, anchor="center")
    tree.grid(row=1, column=0, sticky="nswe")
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
        self.thread_send_settings = None
        self.running_monitor_thread = False
        self.flags = None
        self.thread_stop_print = None
        self.monitor_running = False
        self.thread_monitor = None
        self.button_refresh = None
        self.frame_plot = None
        self.callbacks = kwargs.get("callbacks", {})
        self.file_handler = None
        self.plotter = None
        self.thread_start_print = None
        self.is_sliced = False
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.is_printing = False
        settings = read_settings()
        self.is_settings_sent = False
        self.is_sending = False
        self.frame_process_print = None
        self.is_process_set = False
        self.test_connection = kwargs.get("callbacks", {}).get("test_connection_callback", None)
        # image_capture = Image.open(r"files/img/capture.png")
        # image_capture = image_capture.resize((40, 40))
        # self.icon_capture = ImageTk.PhotoImage(image_capture)
        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_main_info.columnconfigure((0, 1, 2), weight=1)
        self.frame_main_info.rowconfigure(0, weight=1)

        self.load_solid_viewer()
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
        self.frame_buttons.columnconfigure((0, 1, 2, 3, 4), weight=1)
        # frame_btn_img = ttk.LabelFrame(self.frame_buttons)
        # frame_btn_img.grid(row=0, column=0, sticky="n", padx=15, pady=1)
        # ttk.Button(
        #     frame_btn_img,
        #     text="Capture Screenshot",
        #     image=self.icon_capture,
        #     command=self.capture_screen_callback,
        #     style="primary.TButton",
        # ).grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        ttk.Button(
            self.frame_buttons,
            text="Set Printing Process",
            command=self.callback_print_process,
            style="secondary.TButton",
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        ttk.Button(
            self.frame_buttons,
            text="Send settings",
            command=self.send_settings_callback,
            style="primary.TButton",
        ).grid(row=0, column=1, sticky="n", padx=15, pady=15)
        ttk.Button(
            self.frame_buttons,
            text="Send Settings and Files",
            command=self.resend_callback,
            style="secondary.TButton",
        ).grid(row=0, column=2, sticky="n", padx=15, pady=15)
        self.print_button = ttk.Button(
            self.frame_buttons,
            text="Print",
            command=self.print_callback,
            style="success.TButton",
        )
        self.print_button.grid(row=0, column=3, sticky="n", padx=15, pady=15)
        self.stop_button = ttk.Button(
            self.frame_buttons,
            text="Stop",
            command=self.stop_callback,
            style="danger.TButton",
        )
        self.stop_button.grid(row=0, column=4, sticky="n", padx=15, pady=15)
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

    def load_solid_viewer(self):
        settings = read_settings()
        if self.frame_plot is not None:
            self.frame_plot.destroy()
        filepath_stl = settings.get("filepath", "files/pyramid_test.stl")
        n_parts = len(settings.get("sequence", []))
        try:
            os.path.exists(filepath_stl)
            from templates.AuxFunctionsPlots import read_stl
            solid_trimesh_part, solid_part = read_stl(
                file_path=settings.get("filepath", "files/pyramid_test.stl"),
                scale=settings.get("scale"),
                rotation=settings.get("rotation"),
                traslation=settings.get("traslation"),
            )
            from templates.GUI.PlotFrame import SolidViewer
            self.frame_plot = SolidViewer(
                self.frame_main_info, solid_trimesh_part=solid_trimesh_part, parts=n_parts
            )
            self.frame_plot.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        except Exception as e:
            if self.button_refresh is not None:
                self.button_refresh.destroy()
            self.button_refresh = ttk.Button(
                self.frame_main_info, text="Read STL", command=self.import_file_stl
            )
            self.button_refresh.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            print("error reading solid viewer", e)

    def import_file_stl(self):
        settings = read_settings()
        filepath_stl = settings.get("filepath", "files/pyramid_test.stl")
        n_parts = len(settings.get("sequence", []))
        try:
            os.path.exists(filepath_stl)
            from templates.AuxFunctionsPlots import read_stl
            solid_trimesh_part, solid_part = read_stl(
                file_path=settings.get("filepath", "files/pyramid_test.stl"),
                scale=settings.get("scale"),
                rotation=settings.get("rotation"),
                traslation=settings.get("traslation"),
            )
            from templates.GUI.PlotFrame import SolidViewer
            self.frame_plot = SolidViewer(
                self.frame_main_info, solid_trimesh_part=solid_trimesh_part, parts=n_parts
            )
            self.frame_plot.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
            if self.button_refresh is not None:
                self.button_refresh.destroy()
        except Exception as e:
            if self.button_refresh is not None:
                return
            self.button_refresh = ttk.Button(
                self.frame_main_info, text="Read STL", command=self.import_file_stl
            )
            print(e)

    def capture_screen_callback(self):
        if self.file_handler is None:
            from templates.daemons.TempFilesHandler import TempFilesHandler
            self.file_handler = TempFilesHandler()
        self.file_handler.capture_screen()

    def check_parameter_settings(self, settings=None):
        settings = read_settings() if settings is None else settings
        param_list = ["sequence"]
        status_frames = settings.get("status_frames", [0, 0, 0, 0])
        status_frames[2] = 1
        for param in param_list:
            if param not in settings.keys():
                status_frames[2] = 0
                break
        self.callbacks["change_tab_text"](status_frames, "from fprinting")
        update_settings(status_frames=status_frames)
        self.load_solid_viewer()

    def print_callback(self):
        if not self.is_sliced:
            Messagebox.show_error("Settings not sent", "Error")
            return
        if self.is_printing:
           print("Print already in progress")
        # Asegurar que no haya otro hilo `start print` en ejecución
        print("Start printing init")
        if self.thread_start_print and self.thread_start_print.is_alive():
            print("Esperando a que termine el hilo anterior...")
            self.thread_start_print.join()
        # Iniciar nuevo hilo de impresión
        self.thread_start_print = threading.Thread(target=send_start_print)
        self.thread_start_print.start()
        self.thread_monitor = threading.Thread(target=self.monitor_projector, daemon=True)
        self.thread_monitor.start()

        # Iniciar el hilo de monitoreo
        if not self.monitor_running:
            self.monitor_running = True
            self.thread_monitor = threading.Thread(target=self.monitor_response)
            self.thread_monitor.start()

    def monitor_projector(self):
        if self.flags is None:
            self.flags = read_flags()
            self.flags["is_printing"] = True
            self.flags["is_complete"] = False
        self.running_monitor_thread = True
        settings = read_settings()
        delta_layer = settings.get("delta_layer")
        sleep(1)
        while self.running_monitor_thread:
            print("is monitor running: ", self.running_monitor_thread)
            if not self.running_monitor_thread:  # Salida inmediata si se detiene el monitor
                break
            num_layers = self.flags.get("num_layers", 1)
            num_layers  = num_layers if num_layers > 0 else 1
            layer_count = self.flags.get("layer_count", 0)
            is_complete = self.flags.get("is_complete")
            percentage = int((layer_count / num_layers) * 100)
            is_printing = self.flags.get("is_printing")
            # update meter status
            # print(num_layers, layer_count, percentage, is_printing, is_complete)
            if is_complete and not is_printing:
                print("Printing completed")
                percentage = 100
                self.running_monitor_thread = False
                status_frames = settings.get("status_frames")
                status_frames[3] = 1
                update_settings(status_frames=status_frames)
                self.callbacks["change_tab_text"](status_frames, "from complete")
                self.callbacks["save_project_callback"]()
                break
            self.status_widgets[0].configure(amountused=percentage)
            self.test_connection()
            self.flags = read_flags()
            time.sleep(delta_layer / 2)

    def stop_callback(self):
        if not self.is_printing:
            print("Print not in progress")
        print("Stop printing init")
        self.running_monitor_thread = False
        # Asegurar que no haya otro hilo `stop print` en ejecución
        if self.thread_stop_print and self.thread_stop_print.is_alive():
            print("Esperando a que termine el hilo anterior...")
            self.thread_stop_print.join()
        # Iniciar nuevo hilo de impresión
        self.thread_stop_print = threading.Thread(target=send_stop_print)
        self.thread_stop_print.start()

        # Iniciar el hilo de monitoreo
        if not self.monitor_running:
            self.monitor_running = True
            self.thread_monitor = threading.Thread(target=self.monitor_response)
            self.thread_monitor.start()

    def monitor_response(self):
        """Monitorea la respuesta sin crear múltiples hilos innecesarios"""
        while self.monitor_running:
            try:
                status, data = response_queue.get(timeout=1)  # Esperar respuesta

                if status == 200:
                    print(f"Start successful: {data}")
                else:
                    print(f"Error in request: {status}")

                break  # Terminar el monitoreo después de recibir la respuesta

            except queue.Empty:
                time.sleep(0.5)  # Esperar antes de volver a intentar

        print("Deteniendo hilo de monitoreo...")

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
        self.callbacks["change_tab_text"](status_frames, "from print process")

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
        if self.thread_send_settings and self.thread_send_settings.is_alive():
            print("Esperando a que termine el hilo anterior...")
            self.thread_send_settings.join()
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
        self.thread_send_settings = threading.Thread(target=send_settings_printer)
        self.thread_send_settings.start()
        print("Start sending settings")

        self.is_sliced = True
        return 200, "ok"

    def resend_callback(self):
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
        from templates.daemons.TempFilesHandler import TempFilesHandler
        self.file_handler = TempFilesHandler(
            "files/img", zip_file_name, self, "compress"
        )
        self.file_handler.start()
        return 200, "ok"

    def refresh_resume_widgets(self):
        settings = read_settings()
        filepath = settings.get("filepath", "No filepath")
        self.resume_widgets[0].set(value=filepath.split("/")[-1])
        self.resume_widgets[1].set(value=str(settings.get("width_part", "0.0")))
        self.resume_widgets[2].set(value=str(settings.get("height_part", "0.0")))
        self.resume_widgets[3].set(value=str(settings.get("depth_part", "0.0")))
        delta_layer = settings.get("delta_layer")  # seconds
        layers = settings.get("num_layers")
        b_layers = settings.get("b_layers")
        e_time_b_layers = settings.get("e_time_b_layers")
        estimated_time = delta_layer * (layers-b_layers) + b_layers * e_time_b_layers
        hours = int(estimated_time / 3600)
        minutes = int((estimated_time % 3600) / 60)
        seconds = int(estimated_time % 60)
        self.resume_widgets[4].set(value=f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds")
        sequence = settings.get("sequence", [])
        self.resume_widgets[-1].delete(*self.resume_widgets[-1].get_children())
        for step in sequence:
            self.resume_widgets[-1].insert(
                "", "end", values=(step["deposit"], step["height_z"])
            )


class SubFrameBars(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)

        # ----------------------widgets----------------------
        ttk.Label(self, text="Tank 1", style="Custom.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tank1 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
            style="Custom.Horizontal.TProgressbar",
        )
        self.tank1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 2", style="Custom.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.tank2 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
            style="Custom.Horizontal.TProgressbar",
        )
        self.tank2.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 3", style="Custom.TLabel").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.tank3 = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        self.tank3.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Label(self, text="Tank 4", style="Custom.TLabel").grid(row=6, column=0, sticky="w", padx=5, pady=5)
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
