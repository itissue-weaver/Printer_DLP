# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 18/feb/2025  at 22:11 $"

import ttkbootstrap as ttk

from files.constants import font_title, font_entry
from templates.AuxiliarFunctions import update_settings, read_settings


def create_input_widgets_biomaterial(master):
    settings = read_settings()
    entries = []
    frame_inputs = ttk.LabelFrame(master, text="Parameters Biomaterials")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)

    # ----------------------parameters Biomaterials--------------------
    ttk.Label(frame_inputs, text="Tank 1:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_material1 = ttk.StringVar(value=str(settings.get("material1", "Water")))
    ttk.Entry(frame_inputs, textvariable=entry_material1).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_material1)
    ttk.Label(frame_inputs, text="Quantity [ml]:").grid(
        row=0, column=2, sticky="w", padx=10, pady=10
    )
    entry_quantity1 = ttk.StringVar(value=str(settings.get("quantity1", "100")))
    ttk.Entry(frame_inputs, textvariable=entry_quantity1).grid(
        row=0, column=3, sticky="w", padx=5, pady=5
    )
    entries.append(entry_quantity1)
    ttk.Label(frame_inputs, text="Tank 2:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_material2 = ttk.StringVar(value=str(settings.get("material2", "Water")))
    ttk.Entry(frame_inputs, textvariable=entry_material2).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_material2)
    ttk.Label(frame_inputs, text="Quantity [ml]:").grid(
        row=1, column=2, sticky="w", padx=10, pady=10
    )
    entry_quantity2 = ttk.StringVar(value=str(settings.get("quantity2", "100")))
    ttk.Entry(frame_inputs, textvariable=entry_quantity2).grid(
        row=1, column=3, sticky="w", padx=5, pady=5
    )
    entries.append(entry_quantity2)
    ttk.Label(frame_inputs, text="Tank 3:").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_material3 = ttk.StringVar(value=str(settings.get("material3", "Water")))
    ttk.Entry(frame_inputs, textvariable=entry_material3).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_material3)
    ttk.Label(frame_inputs, text="Quantity [ml]:").grid(
        row=2, column=2, sticky="w", padx=10, pady=10
    )
    entry_quantity3 = ttk.StringVar(value=str(settings.get("quantity3", "100")))
    ttk.Entry(frame_inputs, textvariable=entry_quantity3).grid(
        row=2, column=3, sticky="w", padx=5, pady=5
    )
    entries.append(entry_quantity3)
    ttk.Label(frame_inputs, text="Tank 4:").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_material4 = ttk.StringVar(value=str(settings.get("material4", "Water")))
    ttk.Entry(frame_inputs, textvariable=entry_material4).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_material4)
    ttk.Label(frame_inputs, text="Quantity [ml]:").grid(
        row=3, column=2, sticky="w", padx=10, pady=10
    )
    entry_quantity4 = ttk.StringVar(value=str(settings.get("quantity4", "100")))
    ttk.Entry(frame_inputs, textvariable=entry_quantity4).grid(
        row=3, column=3, sticky="w", padx=5, pady=5
    )
    entries.append(entry_quantity4)
    return entries


class SubFrameFormulaBiomaterial(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.title("Biomaterials")
        self.master = master
        self.frame = SubFrameFormulaBiomaterialNormal(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        #  ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Aceptar",
            command=lambda: self.on_close(),
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        # Interceptar el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.frame.on_close()
        self.master.init_levels()
        self.destroy()


class SubFrameFormulaBiomaterialNormal(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(0, weight=1)
        self.entries = create_input_widgets_biomaterial(self.frame_inputs)

    def on_close(self):
        # Obtener los valores de las entradas
        material1 = self.entries[0].get()
        quantity1 = float(self.entries[1].get())
        material2 = self.entries[2].get()
        quantity2 = float(self.entries[3].get())
        material3 = self.entries[4].get()
        quantity3 = float(self.entries[5].get())
        material4 = self.entries[6].get()
        quantity4 = float(self.entries[7].get())
        update_settings(
            material1=material1,
            quantity1=quantity1,
            material2=material2,
            quantity2=quantity2,
            material3=material3,
            quantity3=quantity3,
            material4=material4,
            quantity4=quantity4,
        )


def create_input_widgets_tanks_properties(master):
    settings = read_settings()
    entries = []
    frame_inputs = ttk.LabelFrame(master, text="Parameters Tanks")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure(0, weight=1)
    # ----------------------parameters Tanks--------------------
    frame1 = ttk.LabelFrame(frame_inputs, text="Tank 1")
    frame1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame1.columnconfigure((0, 1), weight=1)
    ttk.Label(frame1, text="Max level [ml]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_max_level1 = ttk.StringVar(value=str(settings.get("max_level1", 10)))
    ttk.Entry(frame1, textvariable=entry_max_level1).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_max_level1)
    ttk.Label(frame1, text="Shape:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_shape1 = ttk.StringVar(value=str(settings.get("shape1", "Cylinder")))
    ttk.Combobox(
        frame1,
        values=["Cylinder", "Rectangle"],
        textvariable=entry_shape1,
        state="readonly",
    ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_shape1)
    text1 = ttk.StringVar(value="Dimensions <None, radius, Height>[cm]:")
    entries.append(text1)
    ttk.Label(frame1, textvariable=text1).grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_dimensions1 = ttk.StringVar(
        value=", ".join(
            [str(item) for item in settings.get("dimensions1", [0.0, 1.0, 1.0])]
        )
    )
    ttk.Entry(frame1, textvariable=entry_dimensions1).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dimensions1)
    frame2 = ttk.LabelFrame(frame_inputs, text="Tank 2")
    frame2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame2.columnconfigure((0, 1), weight=1)
    ttk.Label(frame2, text="Max level [ml]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_max_level2 = ttk.StringVar(value=str(settings.get("max_level2", 10)))
    ttk.Entry(frame2, textvariable=entry_max_level2).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_max_level2)
    ttk.Label(frame2, text="Shape:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_shape2 = ttk.StringVar(value=str(settings.get("shape2", "Cylinder")))
    ttk.Combobox(
        frame2,
        values=["Cylinder", "Rectangle"],
        textvariable=entry_shape2,
        state="readonly",
    ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_shape2)
    text2 = ttk.StringVar(value="Dimensions <None, radius, Height>[cm]:")
    entries.append(text2)
    ttk.Label(frame2, textvariable=text2).grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_dimensions2 = ttk.StringVar(
        value=", ".join(
            [str(item) for item in settings.get("dimensions2", [0.0, 1.0, 1.0])]
        )
    )
    ttk.Entry(frame2, textvariable=entry_dimensions2).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dimensions2)
    frame3 = ttk.LabelFrame(frame_inputs, text="Tank 3")
    frame3.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame3.columnconfigure((0, 1), weight=1)
    ttk.Label(frame3, text="Max level [ml]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_max_level3 = ttk.StringVar(value=str(settings.get("max_level3", 10)))
    ttk.Entry(frame3, textvariable=entry_max_level3).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_max_level3)
    ttk.Label(frame3, text="Shape:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_shape3 = ttk.StringVar(value=str(settings.get("shape3", "Cylinder")))
    ttk.Combobox(
        frame3,
        values=["Cylinder", "Rectangle"],
        textvariable=entry_shape3,
        state="readonly",
    ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_shape3)
    text3 = ttk.StringVar(value="Dimensions <None, radius, Height>[cm]:")
    entries.append(text3)
    ttk.Label(frame3, textvariable=text3).grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_dimensions3 = ttk.StringVar(
        value=", ".join(
            [str(item) for item in settings.get("dimensions3", [0.0, 1.0, 1.0])]
        )
    )
    ttk.Entry(frame3, textvariable=entry_dimensions3).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dimensions3)
    frame4 = ttk.LabelFrame(frame_inputs, text="Tank 4")
    frame4.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
    frame4.columnconfigure((0, 1), weight=1)
    ttk.Label(frame4, text="Max level [ml]:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_max_level4 = ttk.StringVar(value=str(settings.get("max_level4", 10)))
    ttk.Entry(frame4, textvariable=entry_max_level4).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_max_level4)
    ttk.Label(frame4, text="Shape:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_shape4 = ttk.StringVar(value=str(settings.get("shape4", "Cylinder")))
    ttk.Combobox(
        frame4,
        values=["Cylinder", "Rectangle"],
        textvariable=entry_shape4,
        state="readonly",
    ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_shape4)
    text4 = ttk.StringVar(value="Dimensions <None, radius, Height>[cm]:")
    entries.append(text4)
    ttk.Label(frame4, textvariable=text4).grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_dimensions4 = ttk.StringVar(
        value=", ".join(
            [str(item) for item in settings.get("dimensions4", [0.0, 1.0, 1.0])]
        )
    )
    ttk.Entry(frame4, textvariable=entry_dimensions4).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_dimensions4)
    return entries


class SubFrameConfigTanks(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.title("Tanks")
        self.master = master
        self.frame = SubFrameConfigTanksNormal(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        #  ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Aceptar",
            command=lambda: self.on_close(),
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        # Interceptar el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.frame.on_close()
        self.master.init_levels()
        self.destroy()


class SubFrameConfigTanksNormal(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        # ----------------------widgets----------------------
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(0, weight=1)
        self.entries = create_input_widgets_tanks_properties(self.frame_inputs)
        self.entries[1].trace_add(
            "write", callback=lambda *args: self.on_selected_shape(*args, lindex=1)
        )
        self.entries[5].trace_add(
            "write", callback=lambda *args: self.on_selected_shape(*args, lindex=2)
        )
        self.entries[9].trace_add(
            "write", callback=lambda *args: self.on_selected_shape(*args, lindex=3)
        )
        self.entries[13].trace_add(
            "write", callback=lambda *args: self.on_selected_shape(*args, lindex=4)
        )

    def on_selected_shape(self, *args, lindex):
        options = {
            "Cylinder": "Dimensions <None, radius, Height>[cm]:",
            "Rectangle": "Dimensions <Width, Depth, Height>[cm]:",
        }
        match lindex:
            case 1:
                self.entries[2].set(options[self.entries[1].get()])
            case 2:
                self.entries[6].set(options[self.entries[5].get()])
            case 3:
                self.entries[10].set(options[self.entries[9].get()])
            case 4:
                self.entries[14].set(options[self.entries[13].get()])

    def on_close(self):
        # Obtener los valores de las entradas
        max_level1 = float(self.entries[0].get())
        shape1 = self.entries[1].get()
        dimensions1 = [float(item) for item in self.entries[3].get().split(",")]
        max_level2 = float(self.entries[4].get())
        shape2 = self.entries[5].get()
        dimensions2 = [float(item) for item in self.entries[7].get().split(", ")]
        max_level3 = float(self.entries[8].get())
        shape3 = self.entries[9].get()
        dimensions3 = [float(item) for item in self.entries[11].get().split(", ")]
        max_level4 = float(self.entries[12].get())
        shape4 = self.entries[13].get()
        dimensions4 = [float(item) for item in self.entries[15].get().split(", ")]

        update_settings(
            max_level1=max_level1,
            shape1=shape1,
            dimensions1=dimensions1,
            max_level2=max_level2,
            shape2=shape2,
            dimensions2=dimensions2,
            max_level3=max_level3,
            shape3=shape3,
            dimensions3=dimensions3,
            max_level4=max_level4,
            shape4=shape4,
            dimensions4=dimensions4,
        )


class SubFrameConfigBiomaterials(ttk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.title("Tanks")
        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame = SubFrameConfigBiomaterialsNormal(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame.columnconfigure(0, weight=1)
        #  ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Aceptar",
            command=lambda: self.on_close(),
            style="Custom.TButton",
        ).grid(row=0, column=0, sticky="n", padx=15, pady=15)
        # Interceptar el evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.frame.on_close()
        self.destroy()


def create_widgets_biomaterials(master):
    entries = []
    entries_layer = []
    frame_ink1 = ttk.LabelFrame(master, text="Tank 1", style="Custom.TLabelframe")
    frame_ink1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_ink1.configure(style="Custom.TLabelframe")
    frame_ink1.columnconfigure((0, 1), weight=1)
    ttk.Label(frame_ink1, text="Layer:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer1 = ttk.StringVar(value="Layer 1")
    ttk.Entry(frame_ink1, textvariable=entry_layer1, font=font_entry).grid(
        row=0, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer1)
    ttk.Label(
        frame_ink1, text="Components [item1, item2, ...]", style="Custom.TLabel"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_components1 = ttk.StringVar(value="Component 1, Component 2")
    ttk.Entry(frame_ink1, textvariable=entry_components1, font=font_entry).grid(
        row=1, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_components1)
    ttk.Label(frame_ink1, text="Layer Thickness [mm]:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_depth1 = ttk.StringVar(value="0.5")
    ttk.Entry(frame_ink1, textvariable=entry_layer_depth1, font=font_entry).grid(
        row=2, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_depth1)
    ttk.Label(frame_ink1, text="Layer exposure [s]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_exposure1 = ttk.StringVar(value="10")
    ttk.Entry(frame_ink1, textvariable=entry_layer_exposure1, font=font_entry).grid(
        row=3, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_exposure1)
    entries.append(entries_layer)

    entries_layer = []
    frame_ink2 = ttk.LabelFrame(master, text="Tank 2", style="Custom.TLabelframe")
    frame_ink2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    frame_ink2.columnconfigure((0, 1), weight=1)
    frame_ink2.configure(style="Custom.TLabelframe")
    ttk.Label(frame_ink2, text="Layer:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer2 = ttk.StringVar(value="Layer 2")
    ttk.Entry(frame_ink2, textvariable=entry_layer2, font=font_entry).grid(
        row=0, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer2)
    ttk.Label(
        frame_ink2, text="Components [item1, item2, ...]", style="Custom.TLabel"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_components2 = ttk.StringVar(value="Component 3, Component 4")
    ttk.Entry(frame_ink2, textvariable=entry_components2, font=font_entry).grid(
        row=1, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_components2)
    ttk.Label(frame_ink2, text="Layer Thickness [mm]:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_depth2 = ttk.StringVar(value="0.5")
    ttk.Entry(frame_ink2, textvariable=entry_layer_depth2, font=font_entry).grid(
        row=2, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_depth2)
    ttk.Label(frame_ink2, text="Layer exposure [s]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_exposure2 = ttk.StringVar(value="10")
    ttk.Entry(frame_ink2, textvariable=entry_layer_exposure2, font=font_entry).grid(
        row=3, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_exposure2)
    entries.append(entries_layer)

    entries_layer = []
    frame_ink3 = ttk.LabelFrame(master, text="Tank 3", style="Custom.TLabelframe")
    frame_ink3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_ink3.columnconfigure((0, 1), weight=1)
    frame_ink3.configure(style="Custom.TLabelframe")
    ttk.Label(frame_ink3, text="Layer:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer3 = ttk.StringVar(value="Layer 3")
    ttk.Entry(frame_ink3, textvariable=entry_layer3, font=font_entry).grid(
        row=0, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer3)
    ttk.Label(
        frame_ink3, text="Components [item1, item2, ...]", style="Custom.TLabel"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_components3 = ttk.StringVar(value="Component 5, Component 6")
    ttk.Entry(frame_ink3, textvariable=entry_components3, font=font_entry).grid(
        row=1, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_components3)
    ttk.Label(frame_ink3, text="Layer Thickness [mm]:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_depth3 = ttk.StringVar(value="0.5")
    ttk.Entry(frame_ink3, textvariable=entry_layer_depth3, font=font_entry).grid(
        row=2, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_depth3)
    ttk.Label(frame_ink3, text="Layer exposure [s]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="we", padx=10, pady=10
    )
    entry_layer_exposure3 = ttk.StringVar(value="10")
    ttk.Entry(frame_ink3, textvariable=entry_layer_exposure3, font=font_entry).grid(
        row=3, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_exposure3)
    entries.append(entries_layer)

    entries_layer = []
    frame_ink4 = ttk.LabelFrame(master, text="Tank 4", style="Custom.TLabelframe")
    frame_ink4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    frame_ink4.configure(style="Custom.TLabelframe")
    frame_ink4.columnconfigure(1, weight=1)
    ttk.Label(frame_ink4, text="Layer:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer4 = ttk.StringVar(value="Layer 4")
    ttk.Entry(frame_ink4, textvariable=entry_layer4, font=font_entry).grid(
        row=0, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer4)
    ttk.Label(
        frame_ink4, text="Components [item1, item2, ...]", style="Custom.TLabel"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_components4 = ttk.StringVar(value="Component 7, Component 8")
    ttk.Entry(frame_ink4, textvariable=entry_components4, font=font_entry).grid(
        row=1, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_components4)
    ttk.Label(
        frame_ink4,
        text="Layer Thickness [mm]:",
        style="Custom.TLabel",
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)
    entry_layer_depth4 = ttk.StringVar(value="0.5")
    ttk.Entry(frame_ink4, textvariable=entry_layer_depth4, font=font_entry).grid(
        row=2, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_depth4)
    ttk.Label(frame_ink4, text="Layer exposure [s]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=10, pady=10
    )
    entry_layer_exposure4 = ttk.StringVar(value="10")
    ttk.Entry(frame_ink4, textvariable=entry_layer_exposure4, font=font_entry).grid(
        row=3, column=1, sticky="we", padx=5, pady=5
    )
    entries_layer.append(entry_layer_exposure4)
    entries.append(entries_layer)
    return entries


class SubFrameConfigBiomaterialsNormal(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.frame_title = ttk.Frame(self)
        self.frame_title.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        ttk.Label(self.frame_title, text="Bioinks", font=font_title).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure((0, 1), weight=1)
        self.entries = create_widgets_biomaterials(self.frame_inputs)

    def on_close(self):
        pass
