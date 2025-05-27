# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 24/may/2025  at 11:38 $"

import threading

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from files.constants import (
    font_entry,
    font_tabs,
    delay_z,
    delay_n, font_entry_display,
)
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
    imgs_path = {
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
    imgs = {}
    for key, path in imgs_path.items():
        try:
            img = Image.open(path)
        except FileNotFoundError:
            path = imgs_path["default"]
            img = Image.open(path)
        img = img.resize((50, 50))
        imgs[key] = ImageTk.PhotoImage(img)
    return imgs


def create_widgets(master, **kwargs):
    entries = []
    frame_platform = ttk.Labelframe(master, text="Platform Control")
    frame_platform.configure(style="Custom.TLabelframe")
    frame_platform.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_platform.columnconfigure((0, 1), weight=1)
    frame_platform.rowconfigure((1, 2, 3, 4), weight=1)
    ttk.Label(frame_platform, text="Displacement[mm]: ", style="Custom.TLabel").grid(
        row=1, column=0, sticky="nsew", pady=5
    )
    svar_displacement = ttk.StringVar(value="8")
    entries.append(svar_displacement)
    ttk.Entry(
        frame_platform,
        textvariable=svar_displacement,
        style="Custom.TEntry",
        font=font_entry_display,
    ).grid(row=1, column=1, sticky="nsew", pady=5)
    ttk.Label(
        frame_platform, text="Delay step (Speed) [s]: ", style="Custom.TLabel"
    ).grid(row=2, column=0, sticky="nsew", pady=5)
    svar_delay_z = ttk.StringVar(value="0.005")
    ttk.Entry(
        frame_platform,
        textvariable=svar_delay_z,
        style="Custom.TEntry",
        font=font_entry_display,
    ).grid(row=2, column=1, sticky="nsew    ", pady=5)
    ttk.Button(
        frame_platform,
        image=kwargs.get("imgs")["arrow_up"],
        command=lambda: kwargs.get("up_callback")(
            svar_displacement.get(), svar_delay_z.get()
        ),
        text="Up",
        compound="right",
        style="success.TButton",
    ).grid(row=3, column=0, sticky="nswe", pady=10, padx=10)
    ttk.Button(
        frame_platform,
        image=kwargs.get("imgs")["arrow_up"],
        command=lambda: kwargs.get("up_top_callback")(svar_delay_z.get()),
        text="Up sw",
        compound="right",
        style="success.TButton",
    ).grid(row=3, column=1, sticky="nswe", pady=10, padx=10)
    ttk.Button(
        frame_platform,
        image=kwargs.get("imgs")["arrow_down"],
        command=lambda: kwargs.get("down_callback")(
            svar_displacement.get(), svar_delay_z.get()
        ),
        text="Down",
        compound="right",
        style="success.TButton",
    ).grid(row=4, column=0, sticky="nswe", pady=10, padx=10)
    ttk.Button(
        frame_platform,
        image=kwargs.get("imgs")["arrow_down"],
        command=lambda: kwargs.get("down_bottom_callback")(svar_delay_z.get()),
        text="Down sw",
        compound="right",
        style="success.TButton",
    ).grid(row=4, column=1, sticky="nswe", pady=10, padx=10)
    frame_vat = ttk.LabelFrame(master, text="VAT Control", padding=3)
    frame_vat.configure(style="Custom.TLabelframe")
    frame_vat.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    frame_vat.columnconfigure((0, 1), weight=1)
    frame_vat.rowconfigure((0, 1, 2), weight=1)
    ttk.Label(frame_vat, text="Rotation[°]: ", style="Custom.TLabel").grid(
        row=0, column=0, sticky="nsew", pady=5, padx=10
    )
    svar_rotation = ttk.StringVar(value="90")
    ttk.Entry(
        frame_vat, textvariable=svar_rotation, style="Custom.TEntry", font=font_entry_display
    ).grid(row=0, column=1, sticky="nsew", pady=5, padx=10)
    ttk.Label(frame_vat, text="Delay step (Speed) [s]: ", style="Custom.TLabel").grid(
        row=1, column=0, sticky="nsew", pady=5, padx=10
    )
    svar_delay_n = ttk.StringVar(value="0.005")
    ttk.Entry(
        frame_vat, textvariable=svar_delay_n, style="Custom.TEntry", font=font_entry_display
    ).grid(row=1, column=1, sticky="nsew", pady=5, padx=10)
    ttk.Button(
        frame_vat,
        image=kwargs.get("imgs")["rotate"],
        command=lambda: kwargs.get("vat_callback")(
            svar_rotation.get(), svar_delay_n.get()
        ),
        text="Rotation",
        style="success.TButton",
        compound="right",
    ).grid(row=2, column=0, sticky="nswe", pady=10, padx=10)
    entries.append(svar_rotation)
    ttk.Button(
        frame_vat,
        image=kwargs.get("imgs")["rotate"],
        command=lambda: kwargs.get("vat_sw_callback")(svar_delay_n.get()),
        text="Rotation sw",
        style="success.TButton",
        compound="right",
    ).grid(row=2, column=1, sticky="nswe", pady=10, padx=10)

    frame_led = ttk.LabelFrame(master, text="LED Control", padding=3)
    frame_led.configure(style="Custom.TLabelframe")
    frame_led.grid(row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
    frame_led.columnconfigure((0, 1), weight=1)
    frame_led.rowconfigure((0, 1), weight=1)
    ttk.Button(
        frame_led,
        text="ON",
        command=lambda: kwargs.get("led_callback")(True),
        style="success.TButton",
    ).grid(row=0, column=0, sticky="nswe", pady=10, padx=10)
    ttk.Button(
        frame_led,
        text="OFF",
        command=lambda: kwargs.get("led_callback")(False),
        style="danger.TButton",
    ).grid(row=0, column=1, sticky="nswe", pady=10, padx=10)
    ttk.Button(
        frame_led,
        text="Select file",
        command=lambda: kwargs.get("layer_callback")(),
        style="success.TButton",
    ).grid(row=1, column=0, sticky="nswe", pady=10, padx=10)
    svar_layer = ttk.StringVar(value="")
    ttk.Label(frame_led, textvariable=svar_layer, style="Custom.TLabel").grid(
        row=1, column=1, sticky="nsew"
    )
    entries.append(svar_layer)
    return entries


class MainGUIDisplay(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_led = None
        self.thread_motor = None
        self.frame_m_control = None
        self.project_key = None
        self.connected = ttk.BooleanVar(value=False)
        self.title("DLP Bioprinter Control")
        self.style_gui = configure_styles()
        self.after(0, self.maximize_window)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.imgs = load_images()
        kwargs = {
            "up_callback": self.up_callback,
            "down_callback": self.down_callback,
            "vat_callback": self.vat_callback,
            "led_callback": self.led_callback,
            "up_top_callback": self.up_top_callback,
            "down_bottom_callback": self.down_bottom_callback,
            "vat_sw_callback": self.vat_sw_callback,
        }
        # --------------------header-------------------
        self.frame_header = ttk.Frame(self)
        self.frame_header.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        # --------------------body-------------------
        self.frame_body = ttk.Frame(self)
        self.frame_body.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_body.columnconfigure((0, 1), weight=1)
        self.frame_body.rowconfigure(0, weight=1)
        self.entries = create_widgets(self.frame_body, imgs=self.imgs, **kwargs)
        # --------------------footer-------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_footer.columnconfigure((0, 1, 2), weight=1)
        self.button_test = ttk.Button(
            self.frame_footer,
            text="Test Connection",
            command=self.test_connection,
            style="danger.TButton",
            compound="left",
            image=self.imgs["link"],
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
            image=self.imgs.get("close"),
        )
        self.button_config.grid(row=0, column=2, sticky="e", padx=15, pady=15)

    def on_close(self):
        self.destroy()
        self.quit()

    def maximize_window(self):
        try:
            self.state("zoomed")
        except Exception  as e:
            print(e)
            self.attributes("-zoomed", True) # maximize
            # self.attributes("-fullscreen", True) # hide title bar

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

    def test_connection(self):
        try:
            code, data = get_settings_printer()
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
