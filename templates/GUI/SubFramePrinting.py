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
        self.labels = []
        self.combo_boxes = []
        self.entries = []
        self.other_widgets_entries = []

        # ----------------------widgets----------------------
        self.frame_main_info = ttk.Frame(self)
        self.frame_main_info.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        self.button_add_step = ttk.Button(
            self.frame_buttons, text="Add Step", command=self.add_step
        )
        self.button_add_step.grid(row=0, column=0, padx=5, pady=5)

        self.button_remove_step = ttk.Button(
            self.frame_buttons, text="Remove Step", command=self.remove_step
        )
        self.button_remove_step.grid(row=0, column=1, padx=5, pady=5)

        self.button_start = ttk.Button(
            self.frame_buttons, text="Save Process", command=self.on_close_subframe
        )
        self.button_start.grid(row=0, column=2, padx=5, pady=5)

        self.init_sequence()
        # caught close window
        self.protocol("WM_DELETE_WINDOW", self.on_close_subframe)

    def init_sequence(self):
        for i, step in enumerate(self.sequence):
            self.add_step()
            self.combo_boxes[i].set(step["deposit"])
            self.entries[i].insert(0, step["height_z"])

    def add_step(self):
        settings = read_settings()
        row_index = len(self.labels)
        label = ttk.Label(self.frame_main_info, text=f"Step {row_index + 1}")
        label.grid(row=row_index, column=0, padx=5, pady=5)
        self.labels.append(label)

        combo_box = ttk.Combobox(
            self.frame_main_info, values=self.deposits, state="readonly"
        )
        combo_box.grid(row=row_index, column=1, padx=5, pady=5)
        combo_box.bind(
            "<<ComboboxSelected>>",
            lambda event, index=row_index: self.on_combo_box_change(event, index),
        )
        self.combo_boxes.append(combo_box)

        label_1 = ttk.Label(self.frame_main_info, text="Height <z>[mm]:")
        label_1.grid(
            row=row_index, column=2, padx=5, pady=5
        )

        entry_0  = ttk.Entry(self.frame_main_info)
        entry_0.grid(row=row_index, column=3, padx=5, pady=5)
        previous_valor = float(self.entries[-1].get())+settings.get("layer_depth", 0.0) if len(self.entries)>0 else 0.0
        entry_0.insert(0, f"{previous_valor}")
        entry_0.configure(state="readonly")

        entry = ttk.Entry(self.frame_main_info)
        entry.grid(row=row_index, column=4, padx=5, pady=5)
        # configuro a bind for on value change
        entry.bind(
            "<FocusOut>",
            lambda event, index=row_index: self.on_value_change_input(event, index),
        )
        self.other_widgets_entries.append([label_1, entry_0])
        self.entries.append(entry)

    def on_value_change_input(self, event, index):
        try:
            value = float(self.entries[index].get())
            print(value, index)
            settings = read_settings()
            if index != len(self.entries)-1:
                next_value = value + settings.get("layer_depth", 0.0)
                print(next_value)
                self.other_widgets_entries[index+1][1].configure(state="normal")
                self.other_widgets_entries[index+1][1].delete(0, "end")
                self.other_widgets_entries[index+1][1].insert(
                    0, f"{next_value}"
                )
                self.other_widgets_entries[index+1][1].configure(state="readonly")
        except ValueError:
            self.entries[index].delete(0, "end")
            self.entries[index].insert(0, "0.0")

    def remove_step(self):
        if self.labels:
            # Eliminar widgets del último paso
            self.labels[-1].destroy()
            self.combo_boxes[-1].destroy()
            self.entries[-1].destroy()
            for widget in self.other_widgets_entries[-1]:
                widget.destroy()
            # Actualizar las listas
            self.other_widgets_entries.pop()
            self.labels.pop()
            self.combo_boxes.pop()
            self.entries.pop()

    def on_combo_box_change(self, event, index):
        deposit = self.combo_boxes[index].get()
        if deposit == "":
            self.entries[index].delete(0, "end")

    def save_sequence_process(self):
        sequence = []
        for i in range(len(self.labels)):
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
        self.save_sequence_process()
        self.master.on_close_print_process()
        self.master.is_process_set = True
        self.destroy()
