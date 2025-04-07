# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:16 $"

import ttkbootstrap as ttk

from templates.GUI.SubFrameConfig import DisplayConfig, PrinterConfig
from templates.daemons.MotorController import MotorController


class FrameConfig(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.controller_motor = None
        self.title("Configurations")
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.master = master
        # ----------------------Frame----------------------
        self.display_frame = DisplayConfig(self)
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=1)
        self.printer_frame = PrinterConfig(self)
        self.printer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=1)
        # ----------------------Button----------------------
        ttk.Button(
            self,
            text="Close",
            command=self.close_callback,
        ).grid(row=2, column=0, sticky="n", padx=10, pady=10)
        ttk.Button(
            self,
            text="Test",
            command=self.on_test_motors,
        ).grid(row=2, column=0, sticky="n", padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close_callback)

    def close_callback(self):
        self.display_frame.on_close()
        self.printer_frame.on_close()
        self.master.on_config_close()
        self.destroy()

    def on_test_motors(self):
        PINS = {
            "DIR_PLATE": 7,
            "STEP_PLATE": 8,
            "DIR_Z": 19,
            "STEP_Z": 26,
            "MODE": (5, 6),
            "EN": (12, 13),
            "SLEEP": 16,
            "SWITCH_2": 2,
            "SWITCH_3": 3,
        }
        if self.controller_motor is None:
            self.controller_motor = MotorController(PINS)
        self.controller_motor.test_init_movement()
