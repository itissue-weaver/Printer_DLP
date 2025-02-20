# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:56 $"


import ttkbootstrap as ttk
from PIL import Image, ImageTk

from templates.GUI.FrameBiomaterials import FrameBiomaterials
from templates.GUI.FramePrinting import FramePrinting
from templates.GUI.FrameSliceFile import SliceFile
from templates.GUI.Frame_ReadFile import ReadFile
from templates.GUI.FrameConfig import FrameConfig


class MainGUI(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DLP Slice")
        self.after(0, lambda: self.state("zoomed"))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        image = Image.open(r"files/img/config.png")
        image = image.resize((50, 50))
        self.icon_config = ImageTk.PhotoImage(image)
        self.frame_config = None
        # --------------------notebook-------------------
        self.frame_content = ttk.Frame(self)
        self.frame_content.grid(
            row=0, column=0, sticky="nsew", padx=(5, 10), pady=(10, 10)
        )
        self.frame_content.columnconfigure(0, weight=1)
        self.frame_content.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        tab2 = SliceFile(self.notebook)
        self.notebook.add(tab2, text="Slicer")
        tab3 = FrameBiomaterials(self.notebook)
        self.notebook.add(tab3, text="Biomateriales")
        tab4 = FramePrinting(self.notebook)
        self.notebook.add(tab4, text="Impresion")
        tab1 = ReadFile(self.notebook)
        self.notebook.add(tab1, text="Geometría")
        # tab5 = FrameConfig(self.notebook)
        # self.notebook.add(tab5, text="Configuración")
        # --------------------footer-------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        ttk.Button(
            self.frame_footer,
            text="Configuración",
            image=self.icon_config,
            compound="left",
            command=self.click_coonfig,
        ).grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

    def click_coonfig(self):
        if self.frame_config is None:
            self.frame_config = FrameConfig(self)

    def on_config_close(self):
        self.frame_config = None
