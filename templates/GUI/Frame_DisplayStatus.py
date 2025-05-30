# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 30/may/2025  at 09:38 $"

import threading
from tkinter import filedialog

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from files.constants import (
    font_tabs,
    delay_z,
    delay_n, font_entry_display,
)
from templates.GUI.FramePrinting import create_widgets_status, SubFrameBars, create_widgets_resume
from templates.midleware.MD_Printer import (
    control_led_from_gui,
    control_motor_from_gui,
    get_settings_printer,
)

font_buttons = ("Sylfaen", 22, "normal")


def configure_styles():
    style = ttk.Style()
    style.configure("Custom.TButton", font=font_buttons)
    style.configure("Custom.TLabel", font=("Sylfaen", 20, "normal"))
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


class DisplayStatus(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        # --------------------header-------------------
        self.frame_header = ttk.Frame(self)
        self.frame_header.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        # --------------------body-------------------
        self.frame_body = ttk.Frame(self)
        self.frame_body.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_body.columnconfigure((0, 1), weight=1)
        self.frame_body.rowconfigure(0, weight=1)

        self.frame_resume = ttk.Frame(self.frame_body)
        self.frame_resume.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_resume.columnconfigure((0, 1), weight=1)
        self.frame_resume.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.resume_widgets = create_widgets_resume(self.frame_resume)

        self.frame_tanks_and_plot = ttk.Frame(self.frame_body)
        self.frame_tanks_and_plot.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.frame_tanks_and_plot.columnconfigure(0, weight=1)
        self.frame_tanks_and_plot.rowconfigure((0, 1, 2, 3), weight=1)
        ttk.Label(
            self.frame_tanks_and_plot, text="Status", style="Custom.TLabel"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.frame_status = ttk.Frame(self.frame_tanks_and_plot)
        self.frame_status.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_status.columnconfigure(0, weight=1)
        self.frame_status.rowconfigure(0, weight=1)
        self.status_widgets = create_widgets_status(self.frame_status)

        ttk.Label(
            self.frame_tanks_and_plot, text="Materials", style="Custom.TLabel"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.frame_tanks = SubFrameBars(self.frame_tanks_and_plot)
        self.frame_tanks.columnconfigure(0, weight=1)
        self.frame_tanks.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame_tanks.grid(row=3, column=0, sticky="nsew", padx=15, pady=15)