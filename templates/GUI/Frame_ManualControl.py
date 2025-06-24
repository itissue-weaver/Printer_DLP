# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 09/April/2025  at 21:36 $"

import re
import threading

import ttkbootstrap as ttk

from files.constants import font_title, delay_z, delay_n, font_entry
from templates.midleware.MD_Printer import control_motor_from_gui, control_led_from_gui, send_start_print_one_image, \
    send_stop_print, send_command_from_gui

from tkinter import filedialog



class ManualControlFrame(ttk.Toplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.title("Manual Control")
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        self.notebook.configure(style="Custom.TNotebook")
        self.tab0 = ManualControl(self, **kwargs)
        self.notebook.add(self.tab0, text="Control")
        self.tab1 = CommandsFrame(self, **kwargs)
        self.notebook.add(self.tab1, text="Commands")
        self.protocol("WM_DELETE_WINDOW", self.close_callback)

    def close_callback(self):
        self.parent.on_m_control_close()
        self.destroy()


def create_widgets_manual(master, icon_a_up, icon_a_down, icon_rotate, icon_rotate_sw, kwargs):
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
        image=icon_rotate_sw,
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
    ttk.Button(
        frame_led,
        text="Send and start printing",
        command=lambda: kwargs.get("print_callback")(),
        style="success.TButton",
    ).grid(row=2, column=0, sticky="n", pady=10)
    ttk.Button(
        frame_led,
        text="Stop",
        command=lambda: kwargs.get("stop_callback")(),
        style="danger.TButton",
    ).grid(row=2, column=1, sticky="n", pady=10, padx=10)
    return entries


class ManualControl(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.path_image = None
        self.thread_stop_print = None
        self.thread_start_print = None
        self.parent = parent
        self.thread_led = None
        self.thread_motor = None
        self.columnconfigure(0, weight=1)
        self.images = kwargs.get("images")
        self.icon_a_up = self.images["arrow_up"]
        self.icon_a_down = self.images["arrow_down"]
        self.icon_rotate = self.images["rotate"]
        self.icon_rotate_sw = self.images["rotate_end"]
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
            "print_callback": self.print_callback,
            "stop_callback": self.stop_callback
        }
        self.entries = create_widgets_manual(
            entries_frame,
            self.icon_a_up,
            self.icon_a_down,
            self.icon_rotate,
            self.icon_rotate_sw,
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
            self.path_image = path
            self.entries[3].set(path.split("/")[-1])
        else:
            self.path_image = None
            self.entries[3].set("No file selected")


    def print_callback(self):
        if self.entries[3].get() == "No file selected" and self.path_image is None:
            print("No file selected")
            return
        try:
            if self.thread_start_print and self.thread_start_print.is_alive():
                print("Esperando a que termine el hilo anterior...")
                self.thread_start_print.join()
            self.thread_start_print = threading.Thread(target=send_start_print_one_image, args=(self.path_image,))
            self.thread_start_print.start()
        except Exception as e:
            print("Error al iniciar el hilo:", e)

    def stop_callback(self):
        if self.thread_stop_print and self.thread_stop_print.is_alive():
            print("Esperando a que termine el hilo anterior...")
            self.thread_stop_print.join()
        # Iniciar nuevo hilo de impresión
        self.thread_stop_print = threading.Thread(target=send_stop_print)
        self.thread_stop_print.start()

    def up_callback(self, displacement, delay__z):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            steps = 200 * int(displacement) / 8
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z", "cw", "top", "z", int(steps), float(delay__z), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            # controlar lo maximo que sube con el switch
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def up_top_callback(self, delay__z):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z_sw", "cw", "top", "z", 0, float(delay__z), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def down_bottom_callback(self, delay__z):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_z_sw", "ccw", "bottom", "z", 0, float(delay__z), delay_n),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def down_callback(self, displacement, delay__z):
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
                    float(delay__z),
                    delay_n,
                ),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def vat_callback(self, rotation, delay__n):
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
                    float(delay__n),
                ),
            )
            self.thread_motor.start()
        else:
            print("Motor is already running... Wait until it finishes")
            if not self.thread_motor.is_alive():
                self.thread_motor.join()
                self.thread_motor = None

    def vat_sw_callback(self, delay__n):
        if self.thread_motor is None or not self.thread_motor.is_alive():
            self.thread_motor = threading.Thread(
                target=control_motor_from_gui,
                args=("move_plate_sw", "cw", "top", "plate", 0, delay_z, float(delay__n)),
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


def create_widget_commands(parent, **kwargs):
    entries = []
    frame_inputs = ttk.Frame(parent)
    frame_inputs.columnconfigure((0, 1), weight=1)
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_commands = ttk.Frame(frame_inputs)
    frame_commands.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    ttk.Label(frame_commands, text="Commands:", font=font_entry, style="Custom.TLabel").grid(
        row=0, column=0, sticky="nsew", padx=5, pady=5
    )
    #* WT+LEDE=1: Habilitar LED
    #* WT+LEDE=0: Deshabilitar LED
    #* WT+LEDS=xxx: Establecer el nivel de brillo del LED, donde xxx es un valor entre 0 y 1023 para PRO4710LC y PRO4710A
    #* WT+LEDR: Devolver el nivel de brillo del LED
    #* WT+GTMP: Obtener la temperatura del LED en grados Celsius, con una precisión de 1°C y un rango de 0-100
    # WT+SLED=1: El LED se enciende automáticamente después del encendido
    #* WT+SLED=0: El LED permanece apagado después del encendido
    #* WT+SBTN=xxx: Establecer el nivel de brillo predeterminado del LED, donde xxx es un valor de brillo
    commands_list = [
        "WT+LEDE=1",
        "WT+LEDE=0",
        "WT+LEDS=",
        "WT+LEDR",
        "WT+GTMP",
        "WT+SLED=1",
        "WT+SLED=0",
        "WT+SBTN=",
    ]
    entry_command = ttk.StringVar(value="")
    # ttk.Entry(frame_commands, textvariable=entry_command, font=font_entry).grid(
    #     row=1, column=0, sticky="nsew", padx=5, pady=5
    # )
    ttk.Combobox(
        frame_commands,
        values=commands_list,
        font=font_entry,
        state="normal",
        textvariable=entry_command,
    ).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    entries.append(entry_command)
    ttk.Button(
        frame_inputs,
        text="Send command",
        command=lambda: kwargs.get("send_callback")(entry_command.get()),
        style="success.TButton",
    ).grid(row=0, column=1, sticky="we", pady=10)
    frame_content = ttk.Frame(parent)
    frame_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    text_out = ttk.ScrolledText(
        frame_content,
        font=font_entry,
        width=40,
        height=25,
        wrap="word",
    )
    text_out.grid(row=0, column=0, sticky="nsew")
    text_out.tag_config("command", foreground="blue", font=("Segoe UI", font_entry[1], "bold"))
    text_out.tag_config("response", foreground="green", font=("Segoe UI", font_entry[1], "italic"))
    text_out.tag_config("error", foreground="red", font=("Segoe UI", font_entry[1], "bold"))
    entries.append(text_out)
    return entries


def clean_answer(msg: str):
    resultados = re.findall(r'<<<(.*?)>>>', msg, re.DOTALL)
    resultados_limpios = [r.strip() for r in resultados if r.strip()]
    return "\n".join(resultados_limpios)



class CommandsFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.master = parent
        self.entries = create_widget_commands(
            self,
            send_callback=self.send_callback,
        )


    def send_callback(self, command: str):
        if command:
            self.entries[1].insert(ttk.END, f"-->S: {command}\n", "command")
            self.entries[1].see(ttk.END)
            self.entries[0].set("")
            code, data = send_command_from_gui("on", command)
            self.entries[1].insert(ttk.END, f"<--R: {clean_answer(data["msg"])}\n", "response")
            self.entries[1].see(ttk.END)
        else:
            print("No command to send")
