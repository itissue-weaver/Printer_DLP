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
from templates.AuxiliarFunctions import read_settings, save_settings_to_project
from templates.GUI.FrameBiomaterials import FrameBiomaterials
from templates.GUI.FrameHome import HomePage
from templates.GUI.FramePrinting import FramePrinting
from templates.GUI.FrameSliceFile import SliceFile
from templates.GUI.Frame_ManualControl import ManualControlFrame
from templates.GUI.Frame_ReadFile import ReadFile
from templates.GUI.FrameConfig import FrameConfig
from templates.GUI.SubFrameInit import GifFrameApp
from templates.midleware.MD_Printer import get_settings_printer


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
    style.configure("Custom.Treeview", font=("Arial", 18), rowheight=30)
    style.configure("Custom.Treeview.Heading", font=("Arial", 18, "bold"))
    style.configure("success.TButton", font=("Arial", 18))
    style.configure("primary.TButton", font=("Arial", 18))
    return style


class MainGUI(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_m_control = None
        self.project_key = None
        self.title("DLP Slice")
        self.style_gui = configure_styles()
        self.after(0, lambda: self.state("zoomed"))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        image_config = Image.open(r"files/img/config.png")
        image_config = image_config.resize((50, 50))
        image_save = Image.open(r"files/img/save_btn.png")
        image_save = image_save.resize((50, 50))
        image_control = Image.open(r"files/img/remote-control.jpg")
        image_control = image_control.resize((50, 50))
        image_link = Image.open(r"files/img/link.png")
        image_link = image_link.resize((50, 50))
        self.icon_control = ImageTk.PhotoImage(image_control)
        self.icon_config = ImageTk.PhotoImage(image_config)
        self.icon_save = ImageTk.PhotoImage(image_save)
        self.icon_link = ImageTk.PhotoImage(image_link)
        self.frame_config = None
        self.connected = ttk.BooleanVar(value=False)
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
        callbacks = {
                "change_tab_text": self.change_tab_text,
                "change_title": self.change_title,
                "init_tabs": self.init_tabs,
                "change_project": self.change_project_key,
            }
        self.tab0 = HomePage(self.notebook, callbacks=callbacks)
        self.notebook.add(self.tab0, text="Home")
        self.tab3 = FrameBiomaterials(self.notebook,  callbacks=callbacks)
        self.notebook.add(self.tab3, text="Biomaterials")
        self.tab1 = ReadFile(self.notebook,  callbacks=callbacks)
        self.notebook.add(self.tab1, text="Geometry")
        self.tab2 = SliceFile(self.notebook,  callbacks=callbacks)
        self.notebook.add(self.tab2, text="Slicer")
        self.tab4 = FramePrinting(self.notebook, callbacks=callbacks)
        self.notebook.add(self.tab4, text="Printing")
        # tab5 = FrameConfig(self.notebook)
        # self.notebook.add(tab5, text="Configuración")
        # --------------------footer-------------------
        self.frame_footer = ttk.Frame(self)
        self.frame_footer.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_footer.columnconfigure((0, 1, 2, 3, 4), weight=1)
        ttk.Button(
            self.frame_footer,
            text="Configuration",
            image=self.icon_config,
            compound="left",
            command=self.click_config,
            style="Custom.TButton",
        ).grid(row=0, column=0, sticky="w", padx=15, pady=15)
        self.button_test = ttk.Button(
            self.frame_footer,
            text="Test Connection",
            command=self.test_connection,
            style="success.TButton",
            compound="left",
            image=self.icon_link,
        )
        self.button_test.grid(row=0, column=1, sticky="e", padx=15, pady=15)
        self.txt_connected = ttk.StringVar(value="Disconnected")
        ttk.Label(
            self.frame_footer,
            textvariable=self.txt_connected,
            font=("Arial", 18),
            style="Custom.TLabel",
        ).grid(row=0, column=2, sticky="w", padx=15, pady=15)
        self.button_save = ttk.Button(
            self.frame_footer,
            text="Save project",
            image=self.icon_save,
            command=self.save_project,
            style="success.TButton",
            compound="left",
        )
        self.button_save.grid(row=0, column=3, sticky="e", padx=15, pady=15)
        self.button_mControl = ttk.Button(
            self.frame_footer,
            text="Manual Control",
            command=self.click_manual_control,
            style="primary.TButton",
            image=self.icon_control,
            compound="left",
        )
        self.button_mControl.grid(row=0, column=4, sticky="e", padx=15, pady=15)
        self.test_connection()

    def change_project_key(self, project_key):
        self.project_key = project_key

    def save_project(self):
        settings = read_settings()
        save_settings_to_project(self.project_key, settings)

    def click_config(self):
        if self.frame_config is None:
            self.frame_config = FrameConfig(self)

    def on_config_close(self):
        self.frame_config = None

    def click_manual_control(self):
        if self.frame_m_control is None:
            self.frame_m_control = ManualControlFrame(self)

    def on_m_control_close(self):
        self.frame_m_control = None

    def show_gif_toplevel(self):
        GifFrameApp(self)

    def change_tab_text(self, status_frame):
        for tab_index, status in enumerate(status_frame):
            match tab_index + 1:
                case 1:
                    new_text = "Biomaterials ❎" if status == 0 else "Biomaterials ✅"
                case 2:
                    new_text = "Geometry  ❎" if status == 0 else "Geometry ✅"
                case 3:
                    new_text = "Slicer  ❎" if status == 0 else "Slicer ✅"
                case 4:
                    new_text = "Printing  ❎" if status == 0 else "Printing ✅"
                case _:
                    print("No se encontró el tab")
                    continue
            self.notebook.tab(tab_index + 1, text=new_text)

    def change_title(self, new_title):
        self.title(new_title)

    def init_tabs(self):
        self.tab3.load_biomaterial(None, True)
        self.tab1.set_geometry_from_file(True)
        self.tab2.check_parameter_settings()
        self.tab4.check_parameter_settings()

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
