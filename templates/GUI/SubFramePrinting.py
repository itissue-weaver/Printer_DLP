# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:23 $"

import ttkbootstrap as ttk


class FramePrinting(ttk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.is_printing = False
        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.print_button = ttk.Button(
            self.frame_buttons,
            text="Print",
            command=self.print_callback,
        )
        self.print_button.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

    def print_callback(self):
        self.is_printing = not self.is_printing
        if self.is_printing:
            self.print_button.config(text="Stop printing")
        else:
            self.print_button.config(text="Print")