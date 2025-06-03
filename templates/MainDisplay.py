# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 24/may/2025  at 11:38 $"

import threading
from time import sleep
from tkinter import filedialog

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from matplotlib.dates import set_epoch

from files.constants import (
    font_tabs,
    delay_z,
    delay_n, font_entry_display,
)
from templates.AuxiliarFunctions import update_settings, update_flags, read_settings, read_flags
from templates.GUI.Frame_DisplayControl import DisplayControl
from templates.GUI.Frame_DisplayStatus import DisplayStatus
from templates.midleware.MD_Printer import (
    control_led_from_gui,
    control_motor_from_gui,
    get_settings_printer, ask_status,
)

font_buttons = ("Sylfaen", 22, "normal")


def configure_styles():
    style = ttk.Style()
    style.configure("Custom.TButton", font=font_buttons)
    style.configure("Custom.TLabel", font=("Sylfaen", 20, "normal"))
    style.configure("TCustom.TLabel", font=("Sylfaen", 20, "bold"))
    style.configure("Custom.TEntry", font=font_entry_display)
    style.configure("Custom.TLabelframe.Label", font=("Sylfaen", 24, "normal"))
    style.configure("Custom.TNotebook.Tab", font=font_tabs)
    style.configure("Custom.TCombobox", font=font_entry_display)
    style.configure("info.TButton", font=font_buttons)
    style.configure("success.TButton", font=font_buttons)
    style.configure("danger.TButton", font=font_buttons)
    style.configure("Custom.Treeview", font=("Sylfaen", 18), rowheight=30)
    style.configure("Custom.Treeview.Heading", font=("Sylfaen", 18, "bold"))
    style.configure("success.TButton", font=font_buttons)
    style.configure("primary.TButton", font=font_buttons)
    style.configure("secondary.TButton", font=font_buttons)
    style.configure("custom.Horizontal.TProgressbar", font=font_entry_display)
    return style


def load_images():
    images_path = {
        "arrow_up": r"files/img/arrow_up.png",
        "arrow_down": r"files/img/arrow_down.png",
        "rotate": r"files/img/rotate-icon.png",
        "config": r"files/img/config.png",
        "save": r"files/img/save_btn.png",
        "control": r"files/img/remote-control.jpg",
        "link": r"files/img/link.png",
        "close":  r"files/img/close.png",
        "default": r"files/img/no_image.png",
    }
    images = {}
    for key, path in images_path.items():
        try:
            img = Image.open(path)
        except FileNotFoundError:
            path = images_path["default"]
            img = Image.open(path)
        img = img.resize((50, 50))
        images[key] = ImageTk.PhotoImage(img)
    return images


class MainGUIDisplay(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = None
        self.flags = None
        self.running_monitor = True
        self.connected = ttk.BooleanVar(value=False)
        self.thread_monitor =  None
        self.title("DLP Bioprinter Control")
        self.style_gui = configure_styles()
        self.after(0, self.maximize_window)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.images = load_images()
        kwargs = {
            "images": self.images,
        }
        # ----------------------test connection-------------------
        self.thread_connection = threading.Thread(target=self.test_connection_md)
        self.thread_connection.start()
        # --------------------header-------------------
        self.frame_header = ttk.Frame(self)
        self.frame_header.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        # --------------------body-------------------
        self.frame_body = ttk.Frame(self)
        self.frame_body.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_body.columnconfigure(0, weight=1)
        self.frame_body.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.frame_body)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        self.notebook.configure(style="Custom.TNotebook")

        self.frame_1 = DisplayStatus(self.notebook, **kwargs)
        self.notebook.add(self.frame_1, text="Status")
        self.frame_2 = DisplayControl(self.notebook, **kwargs)
        self.notebook.add(self.frame_2, text="Control")
        # --------------------footer-------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_footer.columnconfigure((0, 1, 2), weight=1)
        self.button_test = ttk.Button(
            self.frame_footer,
            text="Test Connection",
            command=self.test_connection_md,
            style="danger.TButton",
            compound="left",
            image=self.images["link"],
        )
        self.button_test.grid(row=0, column=0, sticky="e", padx=15, pady=15)
        self.txt_connected = ttk.StringVar(value="Disconnected")
        ttk.Label(
            self.frame_footer,
            textvariable=self.txt_connected,
            font=("Arial", 18),
            style="Custom.TLabel",
        ).grid(row=0, column=1, sticky="w", padx=15, pady=15)
        self.button_config = ttk.Button(
            self.frame_footer,
            text="Close",
            command=self.on_close,
            style="danger.TButton",
            compound="left",
            image=self.images.get("close"),
        )
        self.button_config.grid(row=0, column=2, sticky="e", padx=15, pady=15)
        self.thread_monitor = threading.Thread(target=self.monitor_projector, daemon=True)
        self.thread_monitor.start()


    def on_close(self):
        self.running_monitor = False
        print("closing")
        # if self.thread_monitor.is_alive():
        #     try:
        #         self.thread_monitor.join()
        #     except Exception as e:
        #         print(e)
        # self.thread_connection.join()
        print("closed")
        self.destroy()
        self.quit()

    def maximize_window(self):
        try:
            self.state("zoomed")
        except Exception  as e:
            print(e)
            self.attributes("-zoomed", True) # maximize
            # self.attributes("-fullscreen", True) # hide title bar

    def test_connection_md(self):
        try:
            code, data = ask_status()
            print(code, data)
            self.settings = data.get("data", {}).get("settings")
            self.flags = data.get("data", {}).get("flags")
            if self.settings is not None:
                update_settings(**data.get("settings", {}))
            if self.flags is not None:
                update_flags(**data.get("flags", {}))
        except Exception as e:
            print(e)
            code = 500
        if code == 200:
            self.connected.set(True)
            self.txt_connected.set("Connected")
            self.button_test.configure(style="success.TButton")
        else:
            self.connected.set(False)
            self.txt_connected.set("Disconnected")
            self.button_test.configure(style="danger.TButton")

    # def test_connection_md(self):
    #     def fetch_status():
    #         try:
    #             code, data = ask_status()
    #             print(code, data)
    #             self.settings = data.get("data", {}).get("settings")
    #             self.flags = data.get("data", {}).get("flags")
    #             if self.settings is not None:
    #                 update_settings(**data.get("settings", {}))
    #             if self.flags is not None:
    #                 update_flags(**data.get("flags", {}))
    #         except Exception as e:
    #             print(e)
    #             code = 500
    #
    #         if code == 200:
    #             self.connected.set(True)
    #             self.txt_connected.set("Connected")
    #             self.button_test.configure(style="success.TButton")
    #         else:
    #             self.connected.set(False)
    #             self.txt_connected.set("Disconnected")
    #             self.button_test.configure(style="danger.TButton")
    #
    #     threading.Thread(target=fetch_status, daemon=True).start()

    def monitor_projector(self):
        if self.thread_connection.is_alive():
            self.thread_connection.join()
        if self.settings is None:
            self.settings = read_settings()
            self.flags = read_flags()
        delta_layer = self.settings.get("delta_layer")
        while self.running_monitor:
            print("is monitor running: ", self.running_monitor)
            if not self.running_monitor:  # Salida inmediata si se detiene el monitor
                break
            self.frame_1.on_update_status(self.settings, self.flags)
            self.test_connection_md()
            sleep(delta_layer/2.5)