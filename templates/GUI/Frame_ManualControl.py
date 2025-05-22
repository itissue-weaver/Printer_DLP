# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 09/April/2025  at 21:36 $"

import threading

import ttkbootstrap as ttk

from files.constants import font_title, delay_z, delay_n
from templates.midleware.MD_Printer import control_motor_from_gui, control_led_from_gui

from tkinter import filedialog


class ManualControlFrame(ttk.Toplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.title("Manual Control")
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.main_frame = ManualControl(self, **kwargs)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.close_callback)

    def close_callback(self):
        self.parent.on_m_control_close()
        self.destroy()


def create_widgets_manual(master, icon_a_up, icon_a_down, icon_rotate, kwargs):
    entries = []
    frame_platform = ttk.LabelFrame(
        master, text="Platform Control", style="Custom.TLabelframe", padding=3
    )
    frame_platform.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_platform.columnconfigure((0, 1), weight=1)
    # ttk.Label(master, text="Platform control", style="Custom.TLabel").grid(row=0, column=0, sticky="nsew")
    ttk.Label(frame_platform, text="Displacement[mm]: ", style="Custom.TLabel").grid(
        row=1, column=0, sticky="nsew"
    )
    svar_displacement = ttk.StringVar(value="8")
    entries.append(svar_displacement)
    ttk.Entry(
        frame_platform, textvariable=svar_displacement, style="Custom.TEntry"
    ).grid(row=1, column=1, sticky="nsew")
    ttk.Label(frame_platform, text="Delay z [s]: ", style="Custom.TLabel").grid(
        row=2, column=0, sticky="nsew"
    )
    svar_delay_z = ttk.StringVar(value="0.005")
    ttk.Entry(frame_platform, textvariable=svar_delay_z, style="Custom.TEntry").grid(
        row=2, column=1, sticky="nsew"
    )
    ttk.Button(
        frame_platform,
        image=icon_a_up,
        command=lambda: kwargs.get("up_callback")(
            svar_displacement.get(), svar_delay_z.get()
        ),
        text="Up",
        compound="right",
        style="success.TButton",
    ).grid(row=3, column=0, sticky="n", pady=10)
    ttk.Button(
        frame_platform,
        image=icon_a_up,
        command=lambda: kwargs.get("up_top_callback")(svar_delay_z.get()),
        text="Up sw",
        compound="right",
        style="success.TButton",
    ).grid(row=3, column=1, sticky="n", pady=10, padx=10)
    ttk.Button(
        frame_platform,
        image=icon_a_down,
        command=lambda: kwargs.get("down_callback")(
            svar_displacement.get(), svar_delay_z.get()
        ),
        text="Down",
        compound="right",
        style="success.TButton",
    ).grid(row=4, column=0, sticky="n", pady=10)
    ttk.Button(
        frame_platform,
        image=icon_a_down,
        command=lambda: kwargs.get("down_bottom_callback")(svar_delay_z.get()),
        text="Down sw",
        compound="right",
        style="success.TButton",
    ).grid(row=4, column=1, sticky="n", pady=10, padx=10)

    frame_vat = ttk.LabelFrame(
        master, text="VAT Control", style="Custom.TLabelframe", padding=3
    )
    frame_vat.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_vat.columnconfigure((0, 1), weight=1)
    # ttk.Label(frame_vat, text="VAT control", style="Custom.TLabel").grid(row=4, column=0, sticky="nsew")
    ttk.Label(frame_vat, text="Rotation[°]: ", style="Custom.TLabel").grid(
        row=0, column=0, sticky="nsew"
    )
    svar_rotation = ttk.StringVar(value="90")
    ttk.Entry(frame_vat, textvariable=svar_rotation, style="Custom.TEntry").grid(
        row=0, column=1, sticky="nsew"
    )
    ttk.Label(frame_vat, text="Delay n [s]: ", style="Custom.TLabel").grid(
        row=1, column=0, sticky="nsew"
    )
    svar_delay_n = ttk.StringVar(value="0.005")
    ttk.Entry(frame_vat, textvariable=svar_delay_n, style="Custom.TEntry").grid(
        row=1, column=1, sticky="nsew"
    )
    ttk.Button(
        frame_vat,
        image=icon_rotate,
        command=lambda: kwargs.get("vat_callback")(
            svar_rotation.get(), svar_delay_n.get()
        ),
        text="Rotation",
        style="success.TButton",
    ).grid(row=2, column=0, sticky="n", pady=10)
    entries.append(svar_rotation)
    ttk.Button(
        frame_vat,
        image=icon_rotate,
        command=lambda: kwargs.get("vat_sw_callback")(svar_delay_n.get()),
        text="Rotation sw",
        style="success.TButton",
    ).grid(row=2, column=1, sticky="n", pady=10, padx=10)
    frame_led = ttk.LabelFrame(
        master, text="LED Control", style="Custom.TLabelframe", padding=3
    )
    frame_led.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame_led.columnconfigure((0, 1), weight=1)
    # ttk.Label(master, text="LED control", style="Custom.TLabel").grid(row=7, column=0, sticky="nsew")
    ttk.Label(frame_led, text="ON/OFF: ", style="Custom.TLabel").grid(
        row=0, column=0, sticky="nsew"
    )
    var_led = ttk.BooleanVar(value=False)
    ttk.Checkbutton(
        frame_led,
        style="Roundtoggle.Toolbutton",
        variable=var_led,
        onvalue=True,
        offvalue=False,
    ).grid(row=0, column=1, sticky="nswe", pady=10)
    var_led.trace_add("write", lambda *args: kwargs.get("led_callback")(var_led.get()))
    entries.append(var_led)
    ttk.Button(
        frame_led,
        text="Select file",
        command=lambda: kwargs.get("layer_callback")(),
        style="success.TButton",
    ).grid(row=1, column=0, sticky="n", pady=10)
    svar_layer = ttk.StringVar(value="")
    ttk.Label(frame_led, textvariable=svar_layer, style="Custom.TLabel").grid(
        row=1, column=1, sticky="nsew"
    )
    entries.append(svar_layer)
    return entries


class ManualControl(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.thread_led = None
        self.thread_motor = None
        self.columnconfigure(0, weight=1)
        self.imgs = kwargs.get("imgs")
        self.icon_a_up = self.imgs["arrow_up"]
        self.icon_a_down = self.imgs["arrow_down"]
        self.icon_rotate = self.imgs["rotate"]
        ttk.Label(self, text="Manual Control", font=font_title).grid(
            row=0, column=0, sticky="nsew"
        )
        entries_frame = ttk.Frame(self)
        entries_frame.grid(row=1, column=0, sticky="nsew")
        entries_frame.columnconfigure(0, weight=1)
        kwargs = {
            "up_callback": self.up_callback,
            "down_callback": self.down_callback,
            "vat_callback": self.vat_callback,
            "led_callback": self.led_callback,
            "layer_callback": self.layer_callback,
            "up_top_callback": self.up_top_callback,
            "down_bottom_callback": self.down_bottom_callback,
            "vat_sw_callback": self.vat_sw_callback,
        }
        self.entries = create_widgets_manual(
            entries_frame,
            self.icon_a_up,
            self.icon_a_down,
            self.icon_rotate,
            kwargs=kwargs,
        )

    def layer_callback(self):
        # dialog for file selection
        path = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(
                ("Image files", ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp"]),
                ("all files", "*.*"),
            ),
        )
        if path:
            self.entries[3].set(path)
        else:
            self.entries[3].set("No file selected")

    def up_callback(self, displacement, delayz):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            steps = 200 * int(displacement) / 8
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z", "cw", "top", "z", int(steps), float(delayz), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            # controlar lo maximo que sube con el switch
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def up_top_callback(self, delayz):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z_sw", "cw", "top", "z", 0, float(delayz), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def down_bottom_callback(self, delayz):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z_sw", "ccw", "bottom", "z", 0, float(delayz), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def down_callback(self, displacement, delayz):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            steps = 200 * int(displacement) / 8
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=(
                    "move_z",
                    "ccw",
                    "bottom",
                    "z",
                    int(steps),
                    float(delayz),
                    delay_n,
                ),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def vat_callback(self, rotation, delayn):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            steps = 200 * int(rotation) / 360
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=(
                    "move_plate",
                    "cw",
                    "top",
                    "plate",
                    int(steps),
                    delay_z,
                    float(delayn),
                ),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def vat_sw_callback(self, delayn):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_plate_sw", "cw", "top", "plate", 0, delay_z, float(delayn)),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def led_callback(self, state=False):
        if self.thread_led is None or not self.thread_led.is_alive():
            state = "on" if state else "off"
            self.thread_led = threading.Thread(
                target=control_led_from_gui, args=(state,)
            )
            self.thread_led.start()
        else:
            print("LED is already running... Wait until it finishes")
            if not self.thread_led.is_alive():
                self.thread_led.join()
                self.thread_led = None
