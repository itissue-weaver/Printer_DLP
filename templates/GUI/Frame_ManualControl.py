# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 09/April/2025  at 21:36 $"


import ttkbootstrap as ttk
from PIL import Image, ImageTk

from files.constants import font_title
from templates.midleware.MD_Printer import control_motor_from_gui


class ManualControlFrame(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manual Control")
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.main_frame = ManualControl(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.protocol("WM_DELETE_WINDOW", self.close_callback)

    def close_callback(self):
        self.parent.on_m_control_close()
        self.destroy()

def create_widgets_manual(master, icon_a_up, icon_a_down, icon_rotate, kwargs):
    entries = []

    ttk.Label(master, text="Platform control", style="Custom.TLabel").grid(row=0, column=0, sticky="nsew")
    ttk.Label(master, text="Displacement[mm]: ", style="Custom.TLabel").grid(row=1, column=0, sticky="nsew")
    svar_displacement = ttk.StringVar(value="8")
    entries.append(svar_displacement)
    ttk.Entry(master, textvariable=svar_displacement, style="Custom.TEntry").grid(row=1, column=1, sticky="nsew")
    ttk.Button(
        master,
        image=icon_a_up,
        command=lambda: kwargs.get("up_callback")(svar_displacement.get()),
        text="Up",
        compound="right",
        style="success.TButton"
    ).grid(row=2, column=0, sticky="n")
    ttk.Button(
        master,
        image=icon_a_down,
        command=lambda: kwargs.get("down_callback")(svar_displacement.get()),
        text="Down",
        compound="right",
        style="success.TButton"
    ).grid(row=3, column=0, sticky="n")
    ttk.Label(master, text="VAT control", style="Custom.TLabel").grid(row=4, column=0, sticky="nsew")
    ttk.Label(master, text="Rotation[°]: ", style="Custom.TLabel").grid(row=5, column=0, sticky="nsew")
    svar_rotation = ttk.StringVar(value="90")
    ttk.Entry(master, textvariable=svar_rotation, style="Custom.TEntry").grid(row=5, column=1, sticky="nsew")
    ttk.Button(
        master,
        image=icon_rotate,
        command=lambda: kwargs.get("vat_callback")(svar_rotation.get()),
        text="Rotation",
        style="success.TButton"
    ).grid(row=6, column=0, sticky="n")
    entries.append(svar_rotation)
    return entries



class ManualControl(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        image_a_up = Image.open(r"files/img/arrow_up.png")
        image_a_up = image_a_up.resize((50, 50))
        self.icon_a_up = ImageTk.PhotoImage(image_a_up)
        image_a_down = Image.open(r"files/img/arrow_down.png")
        image_a_down = image_a_down.resize((50, 50))
        self.icon_a_down = ImageTk.PhotoImage(image_a_down)
        image_rotate = Image.open(r"files/img/rotate-icon.png")
        image_rotate = image_rotate.resize((50, 50))
        self.icon_rotate = ImageTk.PhotoImage(image_rotate)
        ttk.Label(self, text="Manual Control", font=font_title).grid(row=0, column=0, sticky="nsew")
        entries_frame = ttk.Frame(self)
        entries_frame.grid(row=1, column=0, sticky="nsew")
        entries_frame.columnconfigure(0, weight=1)
        kwargs = {
            "up_callback": self.up_callback,
            "down_callback": self.down_callback,
            "vat_callback": self.vat_callback,
        }
        self.entries = create_widgets_manual(entries_frame, self.icon_a_up, self.icon_a_down, self.icon_rotate, kwargs=kwargs)


    def up_callback(self, displacement):
        steps = 200 * int(displacement)/8
        response = control_motor_from_gui(
            action="move_z",
            direction="cw",
            location_z="top",
            motor="z",
            steps=int(steps),
        )
        print(response, steps)

    def down_callback(self, displacement):
        steps = 200 * int(displacement)/8
        response = control_motor_from_gui(
            action="move_z",
            direction="ccw",
            location_z="bottom",
            motor="z",
            steps=int(steps),
        )
        print(response, steps)

    def vat_callback(self, rotation):
        steps = 200 * int(rotation)/360
        response = control_motor_from_gui(
            action="move_plate",
            direction="cw",
            motor="plate",
            steps=int(steps),
            location_z="top",
        )
        print(response)
