# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:16 $"
from PIL import Image
import ttkbootstrap as ttk

from templates.AuxiliarFunctions import read_settings
from templates.GUI.SubFrames import SubFrameFormulaBiomaterial, SubFrameConfigTanks

Image.CUBIC = Image.BICUBIC


class FrameBiomaterials(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.master = master
        # ----------------------buttons----------------------
        # Load biomaterials label
        ttk.Label(self, text="Load biomaterials", font=("Arial", 26)).grid(
            row=0, column=0, padx=10, pady=10, sticky="n"
        )
        self.frame_workspace = ttk.Frame(self)
        self.frame_workspace.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_workspace.columnconfigure((0, 1), weight=1)
        self.frame_workspace.rowconfigure(1, weight=1)
        #  ----------------------Levels----------------------
        self.frame_levels = SubFrameMeters(self.frame_workspace)
        self.frame_levels.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.init_levels()
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self.frame_workspace)
        self.frame_buttons.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.rowconfigure((0, 1), weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Customize materials",
            command=self.standard_formula_callback,
        ).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(
            self.frame_buttons,
            text="Customize Tanks",
            command=self.customize_callback,
        ).grid(row=1, column=0, padx=5, pady=5)

    def init_levels(self):
        settings = read_settings()
        self.frame_levels.update_max_level(
            settings.get("max_level1", 100.0),
            settings.get("max_level2", 100.0),
            settings.get("max_level3", 100.0),
            settings.get("max_level4", 100.0),
        )
        self.frame_levels.update_levels(
            settings.get("quantity1", 0.0),
            settings.get("quantity2", 0.0),
            settings.get("quantity3", 0.0),
            settings.get("quantity4", 0.0),
        )
        self.frame_levels.update_subtext_meters(
            settings.get("material1", "Default 1"),
            settings.get("material2", "Default 2"),
            settings.get("material3", "Default 3"),
            settings.get("material4", "Default 4"),
        )

    def standard_formula_callback(self):
        SubFrameFormulaBiomaterial(self)

    def customize_callback(self):
        SubFrameConfigTanks(self)


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
        )
        self.tank1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tank2 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=50,
            metertype="semi",
            subtext="Tank 2",
        )
        self.tank2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.tank3 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=75,
            metertype="semi",
            subtext="Tank 3",
        )
        self.tank3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.tank4 = ttk.Meter(
            self,
            amounttotal=100,
            amountused=100,
            metertype="semi",
            subtext="Tank 4",
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
