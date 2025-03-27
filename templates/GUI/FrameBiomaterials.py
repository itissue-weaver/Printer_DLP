# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:16 $"


from PIL import Image
import ttkbootstrap as ttk

from files.constants import font_title
from templates.AuxiliarFunctions import read_settings, read_materials, update_settings
from templates.GUI.SubFramePlates import FrameImage
from templates.GUI.SubFrames import (
    SubFrameFormulaBiomaterial,
    SubFrameConfigBiomaterials,
)

Image.CUBIC = Image.BICUBIC


class FrameBiomaterials(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.frame_custom = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.master = master
        self.callbacks = kwargs.get("callbacks", {})
        # ----------------------buttons----------------------
        # Load biomaterials label
        ttk.Label(self, text="Load biomaterials", font=font_title).grid(
            row=0, column=0, padx=10, pady=10, sticky="n"
        )
        self.frame_workspace = ttk.Frame(self)
        self.frame_workspace.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_workspace.columnconfigure((0, 1), weight=1)
        self.frame_workspace.rowconfigure(1, weight=1)
        #  ----------------------Levels----------------------
        self.frame_plates = FrameImage(self.frame_workspace)
        self.frame_plates.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        # self.init_levels()
        # self.load_biomaterial(None, True)
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self.frame_workspace)
        self.frame_buttons.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Cartilage I",
            command=lambda: self.load_biomaterial("mode_1"),
            style="info.TButton",
            width=20,
        ).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Cartilage II",
            command=lambda: self.load_biomaterial("mode_2"),
            style="info.TButton",
            width=20,
        ).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Muscoskeletal I",
            command=lambda: self.load_biomaterial("mode_3"),
            style="info.TButton",
            width=20,
        ).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Muscoskeletal II",
            command=lambda: self.load_biomaterial("mode_4"),
            style="info.TButton",
            width=20,
        ).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Custom",
            command=self.customize_callback,
            style="info.TButton",
            width=20,
        ).grid(row=4, column=0, padx=5, pady=5)
        # ttk.Button(
        #     self.frame_buttons,
        #     text="Customize Tanks",
        #     command=self.customize_callback,
        #     style="info.TButton",
        # ).grid(row=1, column=0, padx=5, pady=5)

    def load_biomaterial(self, bioink, is_init=False):
        materials = read_materials()
        settings = read_settings()
        bioink = settings.get("mode_biomaterial", "mode_a") if is_init else bioink
        bio_1 = materials.get("bioink_1", {})
        bio_2 = materials.get("bioink_2", {})
        bio_3 = materials.get("bioink_3", {})
        bio_4 = materials.get("bioink_4", {})
        alpha_b = 50
        is_found = True
        status_frames = settings.get("status_frames")
        match bioink:
            case "mode_1":
                if self.frame_plates is not None:
                    self.frame_plates.destroy()
                materials_seq = [bio_1, bio_2, bio_3, bio_4]
                texts = [
                    f"{item.get('layer')}\n"
                    + " "
                    + "\n ".join(item.get("components", []))
                    for item in materials_seq
                ]
                self.frame_plates = FrameImage(
                    self.frame_workspace,
                    texts,
                    [
                        (255, 0, 0, alpha_b),
                        (0, 255, 0, alpha_b),
                        (0, 0, 255, alpha_b),
                        (155, 155, 0, alpha_b),
                    ],
                )
                self.frame_plates.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            case "mode_2":
                if self.frame_plates is not None:
                    self.frame_plates.destroy()
                materials_seq = [bio_2, bio_3, bio_4, bio_1]
                texts = [
                    f"{item.get('layer')}\n"
                    + " "
                    + "\n ".join(item.get("components", []))
                    for item in materials_seq
                ]
                self.frame_plates = FrameImage(
                    self.frame_workspace,
                    texts,
                    [
                        (0, 255, 0, alpha_b),
                        (0, 0, 255, alpha_b),
                        (155, 155, 0, alpha_b),
                        (255, 0, 0, alpha_b),
                    ],
                )
                self.frame_plates.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            case "mode_3":
                if self.frame_plates is not None:
                    self.frame_plates.destroy()
                materials_seq = [bio_3, bio_4, bio_1, bio_2]
                texts = [
                    f"{item.get('layer')}\n"
                    + " "
                    + "\n ".join(item.get("components", []))
                    for item in materials_seq
                ]
                self.frame_plates = FrameImage(
                    self.frame_workspace,
                    texts,
                    [
                        (0, 0, 255, alpha_b),
                        (155, 155, 0, alpha_b),
                        (255, 0, 0, alpha_b),
                        (0, 255, 0, alpha_b),
                    ],
                )
                self.frame_plates.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            case "mode_4":
                if self.frame_plates is not None:
                    self.frame_plates.destroy()
                materials_seq = [bio_4, bio_1, bio_2, bio_3]
                texts = [
                    f"{item.get('layer')}\n"
                    + " "
                    + "\n ".join(item.get("components", []))
                    for item in materials_seq
                ]
                self.frame_plates = FrameImage(
                    self.frame_workspace,
                    texts,
                    [
                        (155, 155, 0, alpha_b),
                        (255, 0, 0, alpha_b),
                        (0, 255, 0, alpha_b),
                        (0, 0, 255, alpha_b),
                    ],
                )
                self.frame_plates.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            case _:
                print("No se encontro el modo")
                is_found = False
                materials_seq = [bio_1, bio_2, bio_3, bio_4]
        status_frames[0] = 0 if not is_found else 1
        self.callbacks["change_tab_text"](status_frames)
        update_settings(materials=materials_seq, mode_biomaterial=bioink)

    def standard_formula_callback(self):
        SubFrameFormulaBiomaterial(self)

    def customize_callback(self):
        if self.frame_custom is not None:
            self.frame_custom.destroy()
        self.frame_custom = SubFrameConfigBiomaterials(self)
        # allow it to be resizable
        self.frame_custom.attributes("-topmost", True)


class SubFrameMeters(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)
        # ----------------------widgets----------------------
        self.tank1 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=25,
            metertype="semi",
            subtext="Tank 1",
            textright="ml",
            metersize=300,
            textfont=("Arial", 24, "bold"),
            subtextfont=("Cambria", 18),
        )
        self.tank1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tank2 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=50,
            metertype="semi",
            subtext="Tank 2",
            textright="ml",
            metersize=300,
            textfont=("Arial", 24, "bold"),
            subtextfont=("Cambria", 18),
        )
        self.tank2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.tank3 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=75,
            metertype="semi",
            subtext="Tank 3",
            textright="ml",
            metersize=300,
            textfont=("Arial", 24, "bold"),
            subtextfont=("Cambria", 18),
        )
        self.tank3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.tank4 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=100,
            metertype="semi",
            subtext="Tank 4",
            textright="ml",
            metersize=300,
            textfont=("Arial", 24, "bold"),
            subtextfont=("Cambria", 18),
        )
        self.tank4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.update_levels(25, 50, 75, 100)

    def update_levels(self, level1, level2, level3, level4):
        settings = read_settings()
        self.tank1.configure(amountused=level1)
        self.tank2.configure(amountused=level2)
        self.tank3.configure(amountused=level3)
        self.tank4.configure(amountused=level4)
        self.configure_style(self.tank1, level1, settings.get("max_level1", 100.0))
        self.configure_style(self.tank2, level2, settings.get("max_level2", 100.0))
        self.configure_style(self.tank3, level3, settings.get("max_level3", 100.0))
        self.configure_style(self.tank4, level4, settings.get("max_level4", 100.0))

    def configure_style(self, widget, level, max_level):
        if level <= 0.25 * max_level:
            widget.configure(bootstyle="danger")
        elif level <= 0.5 * max_level:
            widget.configure(bootstyle="warning")
        elif level <= 0.75 * max_level:
            widget.configure(bootstyle="info")
        else:
            widget.configure(bootstyle="success")

    def update_subtext_meters(self, text1, text2, text3, text4):
        self.tank1.configure(subtext=text1)
        self.tank2.configure(subtext=text2)
        self.tank3.configure(subtext=text3)
        self.tank4.configure(subtext=text4)

    def update_max_level(self, max_level1, max_level2, max_level3, max_level4):
        self.tank1.configure(amounttotal=max_level1)
        self.tank2.configure(amounttotal=max_level2)
        self.tank3.configure(amounttotal=max_level3)
        self.tank4.configure(amounttotal=max_level4)
