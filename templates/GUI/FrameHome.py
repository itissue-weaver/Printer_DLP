# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 14:21 $"

import ttkbootstrap as ttk
from PIL import ImageTk, Image

from files.constants import font_buttons
from templates.AuxiliarFunctions import read_projects
from templates.GUI.SubFrameInit import GifFrameApp
from templates.midleware.MD_Printer import get_settings_printer


class HomePage(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.connected = ttk.BooleanVar(value=False)
        # ----------------------widgets----------------------
        # ttk.Label(
        #     self,
        #     text="Welcome to the Biomaterials Printer Software",
        #     font=("Arial", 36),
        # ).grid(row=0, column=0, padx=10, pady=10)

        # ------------------------ProjectFilesSelector----------------------
        self.frame_new =  ttk.Frame(self)
        self.frame_new.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Button(
            self.frame_new,
            text="New Project",
            command=self.new_project_callback,
            style="success.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.frame_previous = ttk.Frame(self)
        self.frame_previous.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        projects = read_projects()
        data_lists = [[k, v.get("name"), v.get("timestamp"), v] for k,v in projects.items()]
        self.tv_projects = ttk.Treeview(
            self.frame_previous,
            columns=("name", "timestamp"),
            show="headings",
            style="Custom.Treeview",
        )
        self.tv_projects.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tv_projects.configure(columns=("key", "name", "timestamp", "data"))
        for col in self.tv_projects['columns']:
            self.tv_projects.heading(col, text=col.title(), anchor="w")
        # hide data column
        self.tv_projects.column("data", stretch=False, width=0)
        # insert data
        for item in data_lists:
            self.tv_projects.insert("", "end", values=item)

        # -----------------------footer----------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=2, column=0, sticky="wes", padx=10, pady=10)
        self.txt_connected = ttk.StringVar(value="Disconnected")
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
            style="Custom.TLabel",
        ).grid(row=0, column=1, sticky="w", padx=10, pady=10)
        self.test_connection()

    def new_project_callback(self):
        self.master.change_title("New Project")

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


