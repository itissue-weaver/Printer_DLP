# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/feb/2025  at 21:23 $"

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from templates.AuxiliarFunctions import update_settings, read_settings


class FramePrintingProcess(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Printing Process")
        self.master = master
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.is_printing = False
        self.deposits = ["", 1, 2, 3, 4]
        settings = read_settings()
        self.sequence = settings.get("sequence", [])
        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.labels = []
        self.combo_boxes = []
        self.entries = []

        for i in range(4):  # Assuming we need 4 inputs
            label = ttk.Label(self.frame_main_info, text=f"Step {i + 1}")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.labels.append(label)

            combo_box = ttk.Combobox(
                self.frame_main_info, values=self.deposits, state="readonly"
            )
            combo_box.grid(row=i, column=1, padx=5, pady=5)
            combo_box.bind(
                "<<ComboboxSelected>>",
                lambda event, index=i: self.on_combo_box_change(event, index),
            )
            self.combo_boxes.append(combo_box)
            ttk.Label(self.frame_main_info, text="Height <z>[mm]:").grid(
                row=i, column=2, padx=5, pady=5
            )
            entry = ttk.Entry(self.frame_main_info)
            entry.grid(row=i, column=3, padx=5, pady=5)
            self.entries.append(entry)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        self.button_start = ttk.Button(
            self.frame_buttons, text="Save Process", command=self.callback_button
        )
        self.button_start.grid(row=0, column=0, padx=5, pady=5)
        self.init_sequence()
        # caught close window
        self.protocol("WM_DELETE_WINDOW", self.on_close_subframe)

    def init_sequence(self):
        for i, step in enumerate(self.sequence):
            self.combo_boxes[i].set(step["deposit"])
            self.entries[i].insert(0, step["height_z"])

    def on_combo_box_change(self, event, index):
        deposit = self.combo_boxes[index].get()
        if deposit == "":
            self.entries[index].delete(0, ttk.END)

    def callback_button(self):
        sequence = []
        for i in range(4):
            deposit = self.combo_boxes[i].get()
            height_z = self.entries[i].get()
            if deposit and height_z:
                try:
                    height_z = float(height_z)
                except ValueError:
                    continue  # Ignore entries that are not valid numbers
                sequence.append({"deposit": deposit, "height_z": height_z, "index": i})
        if sequence:
            update_settings(sequence=sequence)
            self.master.is_process_set = True
        else:
            print("No valid sequence entered")
            Messagebox.show_error("No valid sequence entered", "Error")
            self.master.is_process_set = False

    def on_close_subframe(self):
        self.callback_button()
        self.master.on_close_printProccess()
        self.master.is_process_set = True
        self.destroy()
