# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:16 $"

import ttkbootstrap as ttk

from templates.GUI.SubFrameConfig import DisplayConfig, PrinterConfig
from templates.midleware.MD_Printer import test_motor_post


class FrameConfig(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.controller_motor = None
        self.title("Configurations")
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.master = master
        self.warning_var = ttk.StringVar(value="🛑Modifying these values can cause distortion in the layers and final result.")
        # ----------------------Frame----------------------
        self.display_frame = DisplayConfig(self)
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=1)
        self.printer_frame = PrinterConfig(self)
        self.printer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=1)
        ttk.Label(self, textvariable=self.warning_var).grid(row=2, column=0, sticky="n", padx=10, pady=10)
        # ----------------------Button----------------------
        ttk.Button(
            self,
            text="Close",
            command=self.close_callback,
        ).grid(row=3, column=0, sticky="n", padx=10, pady=10)
        # ttk.Button(
        #     self,
        #     text="Test",
        #     command=self.on_test_motors,
        # ).grid(row=2, column=1, sticky="n", padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_callback)

    def close_callback(self):
        self.display_frame.on_close()
        self.printer_frame.on_close()
        self.master.on_config_close()
        self.destroy()

    def on_test_motors(self):
        code, data = test_motor_post()
        print(code, data)
