# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 14:21 $"

import ttkbootstrap as ttk
from PIL import ImageTk, Image

from templates.midleware.MD_Printer import get_settings_printer


class HomePage(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.master = master
        self.connected = ttk.BooleanVar(value=False)
        # ----------------------widgets----------------------
        ttk.Label(
            self,
            text="Welcome to the Biomaterials Printer Software",
            font=("Arial", 36),
        ).grid(row=0, column=0, padx=10, pady=10)
        # ------------------------images----------------------
        image = Image.open(r"files/img/start.jpg")
        width, height = image.size
        new_width = int(width / 7)
        new_height = int(height / 7)
        image = image.resize((new_width, new_height))
        # image = image.resize((4624, 3472))
        self.image_start = ImageTk.PhotoImage(image)
        self.frame_image = ttk.Frame(self)
        self.frame_image.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_image.columnconfigure(0, weight=1)
        self.frame_image.rowconfigure(0, weight=1)

        canvas = ttk.Canvas(self.frame_image, width=new_width, height=new_height)
        canvas.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        canvas.create_image(0, 0, anchor="nw", image=self.image_start)
        # -----------------------footer----------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=2, column=0, sticky="wes", padx=10, pady=10)
        self.txt_connected = ttk.StringVar(value="Disconnected")
        my_style = ttk.Style()
        my_style.configure("success.TButton", font=("Arial", 18))
        self.button_test = ttk.Button(
            self.frame_footer,
            text="Test Connection",
            command=self.test_connection,
            style="success.TButton",
        )
        self.button_test.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(
            self.frame_footer,
            textvariable=self.txt_connected,
            font=("Arial", 18),
        ).grid(row=0, column=1, sticky="w", padx=10, pady=10)
        self.test_connection()

    def test_connection(self):
        try:
            code, data = get_settings_printer()
        except Exception as e:
            print(e)
            code = 500
        if code == 200:
            self.connected.set(True)
            self.txt_connected.set("Connected")
            self.button_test.configure(bootstyle="success")
        else:
            self.connected.set(False)
            self.txt_connected.set("Disconnected")
            self.button_test.configure(bootstyle="danger")
