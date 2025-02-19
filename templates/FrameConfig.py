# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:16 $"

import ttkbootstrap as ttk

from templates.SubFrames import DisplayConfig


class FrameConfig(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=0, column=0, sticky="nsew")
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Display",
            command=self.display_callback,
        ).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Printer",
            command=self.printer_callback,
        ).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def display_callback(self):
        display = DisplayConfig(self)

    def printer_callback(self):
        display = DisplayConfig(self)
