# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:56 $"


import ttkbootstrap as ttk
from PIL import Image, ImageTk

from files.constants import (
    font_buttons,
    font_labels,
    font_labels_frame,
    font_entry,
    font_tabs,
)
from templates.GUI.FrameBiomaterials import FrameBiomaterials
from templates.GUI.FrameHome import HomePage
from templates.GUI.FramePrinting import FramePrinting
from templates.GUI.FrameSliceFile import SliceFile
from templates.GUI.Frame_ReadFile import ReadFile
from templates.GUI.FrameConfig import FrameConfig
from templates.GUI.SubFrameInit import GifFrameApp


def configure_styles():
    style = ttk.Style()
    style.configure("Custom.TButton", font=font_buttons)
    style.configure("Custom.TLabel", font=font_labels)
    style.configure("Custom.TEntry", font=font_entry)
    style.configure("Custom.TLabelframe.Label", font=font_labels_frame)
    style.configure("Custom.TNotebook.Tab", font=font_tabs)
    style.configure("Custom.TCombobox", font=font_entry)
    style.configure("info.TButton", font=font_buttons)
    style.configure("success.TButton", font=("Arial", 18))
    style.configure("danger.TButton", font=("Arial", 18))

    return style


class MainGUI(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DLP Slice")
        self.style_gui = configure_styles()
        self.after(0, lambda: self.state("zoomed"))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        image = Image.open(r"files/img/config.png")
        image = image.resize((50, 50))
        self.icon_config = ImageTk.PhotoImage(image)
        self.frame_config = None
        # --------------------Start Animation -------------------
        # self.show_gif_toplevel()
        # --------------------notebook-------------------
        self.frame_content = ttk.Frame(self)
        self.frame_content.grid(
            row=0, column=0, sticky="nsew", padx=(5, 10), pady=(10, 10)
        )
        self.frame_content.columnconfigure(0, weight=1)
        self.frame_content.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.configure(style="Custom.TNotebook")
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        tab0 = HomePage(self.notebook)
        self.notebook.add(tab0, text="Home")
        tab3 = FrameBiomaterials(self.notebook)
        self.notebook.add(tab3, text="Biomateriales")
        tab1 = ReadFile(self.notebook)
        self.notebook.add(tab1, text="Geometría")
        tab2 = SliceFile(self.notebook)
        self.notebook.add(tab2, text="Slicer")
        tab4 = FramePrinting(self.notebook)
        self.notebook.add(tab4, text="Impresion")

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
            style="Custom.TButton",
        ).grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

    def click_coonfig(self):
        if self.frame_config is None:
            self.frame_config = FrameConfig(self)

    def on_config_close(self):
        self.frame_config = None

    def show_gif_toplevel(self):
        GifFrameApp(self)
