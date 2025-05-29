# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:05 $"

from tkinter import messagebox

import pyslm
import pyslm.visualise
import ttkbootstrap as ttk
from PIL import ImageTk, Image

from files.constants import font_entry
from templates.AuxiliarFunctions import update_settings, read_settings
from templates.GUI.PlotFrame import PlotSTL, ImageFrameApp
from templates.AuxiliarHatcher import build_hatcher


def create_input_widgets(master, **kwargs):
    entries = []
    # ----------------------parameters hatching--------------------
    frame_inputs = ttk.LabelFrame(master, text="Parameters")
    frame_inputs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_inputs.columnconfigure((0, 1, 2, 3), weight=1)
    frame_inputs.configure(style="Custom.TLabelframe")
    frame_geometry = ttk.LabelFrame(frame_inputs, text="Geometry")
    frame_geometry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_geometry.columnconfigure(1, weight=1)
    frame_geometry.configure(style="Custom.TLabelframe")
    ttk.Label(frame_geometry, text="File:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Label(
        frame_geometry, textvariable=kwargs.get("var_path"), style="Custom.TLabel"
    ).grid(row=0, column=1, sticky="ew", columnspan=2, padx=5, pady=5)
    ttk.Label(frame_geometry, text="Rotation[x,y,z]:", style="Custom.TLabel").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    entry_rotation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(frame_geometry, textvariable=entry_rotation, font=font_entry).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_rotation)
    ttk.Label(frame_geometry, text="Scale[x,y,z]:", style="Custom.TLabel").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    entry_scale = ttk.StringVar(value="1.0, 1.0, 1.0")
    ttk.Entry(frame_geometry, textvariable=entry_scale, font=font_entry).grid(
        row=3, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_scale)
    ttk.Label(frame_geometry, text="Translation[x,y,z]:", style="Custom.TLabel").grid(
        row=4, column=0, sticky="w", padx=5, pady=5
    )
    entry_translation = ttk.StringVar(value="0.0, 0.0, 0.0")
    ttk.Entry(frame_geometry, textvariable=entry_translation, font=font_entry).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_translation)

    frame_hatching = ttk.LabelFrame(frame_inputs, text="Hatching")
    frame_hatching.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_hatching.columnconfigure(1, weight=1)
    frame_hatching.configure(style="Custom.TLabelframe")
    ttk.Label(frame_hatching, text="Hatcher type:", style="Custom.TLabel").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatcher_type = ttk.StringVar(value="Base")
    ttk.Combobox(
        frame_hatching,
        values=["Base", "Island", "Stripe"],
        textvariable=entry_hatcher_type,
        state="readonly",
        style="Custom.TCombobox",
    ).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_hatcher_type)
    ttk.Label(frame_hatching, text="Hatch angle [º]:", style="Custom.TLabel").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatch_angle = ttk.StringVar(value="10.0")
    ttk.Entry(frame_hatching, textvariable=entry_hatch_angle, font=font_entry).grid(
        row=1, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_hatch_angle)
    ttk.Label(
        frame_hatching, text="Volume offset hatch [mm]:", style="Custom.TLabel"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)
    entry_volume_offset = ttk.StringVar(value="0.0")
    ttk.Entry(frame_hatching, textvariable=entry_volume_offset, font=font_entry).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_volume_offset)
    ttk.Label(
        frame_hatching, text="Spot compensation [mm]:", style="Custom.TLabel"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)
    entry_spot_compensation = ttk.StringVar(value="0.0")
    ttk.Entry(
        frame_hatching, textvariable=entry_spot_compensation, font=font_entry
    ).grid(row=3, column=1, sticky="w", padx=5, pady=5)
    entries.append(entry_spot_compensation)
    ttk.Label(frame_hatching, text="Inner contours:", style="Custom.TLabel").grid(
        row=4, column=0, sticky="w", padx=10, pady=10
    )
    entry_inner_contours = ttk.StringVar(value="2")
    ttk.Entry(frame_hatching, textvariable=entry_inner_contours, font=font_entry).grid(
        row=4, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_inner_contours)
    ttk.Label(frame_hatching, text="Outer contours:", style="Custom.TLabel").grid(
        row=5, column=0, sticky="w", padx=10, pady=10
    )
    entry_outer_contours = ttk.StringVar(value="1")
    ttk.Entry(frame_hatching, textvariable=entry_outer_contours, font=font_entry).grid(
        row=5, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_outer_contours)
    ttk.Label(frame_hatching, text="Hatch spacing [mm]:", style="Custom.TLabel").grid(
        row=6, column=0, sticky="w", padx=10, pady=10
    )
    entry_hatch_spacing = ttk.StringVar(value="0.5")
    ttk.Entry(frame_hatching, textvariable=entry_hatch_spacing, font=font_entry).grid(
        row=6, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_hatch_spacing)
    ttk.Label(frame_hatching, text="Stripe width [mm]:", style="Custom.TLabel").grid(
        row=7, column=0, sticky="w", padx=10, pady=10
    )
    entry_stripe_width = ttk.StringVar(value="0.5")
    ttk.Entry(frame_hatching, textvariable=entry_stripe_width, font=font_entry).grid(
        row=7, column=1, sticky="w", padx=5, pady=5
    )
    entries.append(entry_stripe_width)
    return entries


def create_buttons(master, **kwargs):
    my_style = ttk.Style()
    my_style.configure("info.TButton", font=("Arial", 18))
    ttk.Button(
        master,
        text="Slice",
        command=kwargs.get("callback_sliceFile", None),
        style="info.TButton",
    ).grid(row=0, column=0, sticky="n")
    ttk.Button(
        master,
        text="Save",
        command=kwargs.get("callback_saveSettings", None),
        style="info.TButton",
    ).grid(row=0, column=1, sticky="n")


def read_stl_frame(**kwargs):
    filepath = kwargs.get("file_path", None)
    if filepath is None:
        return None
    rotation = kwargs.get("rotation", [0, 0, 0])
    scale = kwargs.get("scale", [1, 1, 1])
    translation = kwargs.get("translation", [0, 0, 0])
    update_settings(rotation=rotation, scale=scale, translation=translation)
    solid_part = pyslm.Part("myFrameGuide")
    solid_part.setGeometry(kwargs.get("file_path", None))
    solid_part.rotation = rotation
    solid_part.translation = translation
    solid_part.scale = scale
    solid_part.dropToPlatform()
    return solid_part


def get_geometry_parameters(entries):
    rotation = [float(i) for i in entries[0].get().split(",")]
    scale = [float(i) for i in entries[1].get().split(",")]
    translation = [float(i) for i in entries[2].get().split(",")]
    return rotation, scale, translation


def get_hatching_parameters(entries):
    hatcher_type = entries[3].get()
    hatch_angle = float(entries[4].get())
    volume_offset = float(entries[5].get())
    spot_compensation = float(entries[6].get())
    inner_contours = int(entries[7].get())
    outer_contours = int(entries[8].get())
    hatch_spacing = float(entries[9].get())
    stripe_width = float(entries[10].get())
    return (
        hatcher_type,
        hatch_angle,
        volume_offset,
        spot_compensation,
        inner_contours,
        outer_contours,
        hatch_spacing,
        stripe_width,
    )


def get_display_parameters(entries):
    projector_dimension = [float(i) for i in entries[11].get().split(",")]
    projector_resolution = [int(i) for i in entries[12].get().split(",")]
    projector_offset = [float(i) for i in entries[13].get().split(",")]
    dpi = int(entries[14].get())
    return projector_dimension, projector_resolution, projector_offset, dpi


def get_print_parameters(entries):
    layer_depth = float(entries[15].get())
    delta_layer = float(entries[16].get())
    plate = int(entries[17].get())
    return layer_depth, delta_layer, plate


def create_image_frame(master, canvas):
    if canvas is not None:
        canvas.destroy()
    image = Image.open(r"files/img/temp.png")
    width, height = image.size
    new_width = int(width / 1)
    new_height = int(height / 1)
    image = image.resize((new_width, new_height))
    image_start = ImageTk.PhotoImage(image)
    canvas = ttk.Canvas(master, width=new_width, height=new_height)
    canvas.grid(row=0, column=0, sticky="nswe")
    canvas.create_image(0, 0, anchor="sw", image=image_start)
    return canvas


class SliceFile(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.plotter = None
        self.current_z = None
        self.display_thread = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # ----------------------variables--------------------
        self.entry_z = None
        self.frame_plot = None
        self.callbacks = kwargs.get("callbacks", {})
        settings = read_settings()
        # self.check_parameter_settings(settings)
        filepath = settings.get("filepath")
        self.z_value = 0.0
        self.show_path = ttk.StringVar(
            value=filepath.split("/")[-1] if filepath is not None else "No file selected"
        )
        self.z_max = settings.get("depth_part", 100)
        # self.viewer = DlpViewer()
        # ----------------------widgets----------------------
        self.frame_widgets = ttk.Frame(self)
        self.frame_widgets.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_widgets.columnconfigure(1, weight=1)
        self.frame_widgets.rowconfigure(0, weight=1)
        self.frame_inputs = ttk.Frame(self.frame_widgets)
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_inputs.columnconfigure(0, weight=1)

        self.entries = create_input_widgets(
            self.frame_inputs,
            callback_scale=lambda value: self.scale_callback(value),
            var_path=self.show_path,
        )
        # ----------------------axes---------------------------
        self.frame_axes = ttk.LabelFrame(self.frame_widgets, text="Preview")
        self.frame_axes.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.frame_axes.columnconfigure(0, weight=1)
        self.frame_axes.rowconfigure(0, weight=1)
        self.frame_axes.configure(style="Custom.TLabelframe")
        self.canvas_img = ImageFrameApp(self.frame_axes)
        self.canvas_img.grid(row=0, column=0, sticky="nsew")
        # ----------------------parameters visual--------------------
        frame_visual = ttk.LabelFrame(self, text="Visualization")
        frame_visual.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame_visual.columnconfigure(3, weight=1)
        frame_visual.configure(style="Custom.TLabelframe")
        ttk.Label(frame_visual, text="z:", style="Custom.TLabel").grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )
        entry_z = ttk.DoubleVar(value=0.0)
        ttk.Entry(frame_visual, textvariable=entry_z, font=font_entry).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )
        self.min_value = ttk.StringVar(value="Min: 0.0")
        ttk.Label(frame_visual, textvariable=self.min_value, style="Custom.TLabel").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        ttk.Scale(
            frame_visual,
            from_=0.0,
            to=self.z_max,
            orient="horizontal",
            command=self.scale_callback,
            variable=entry_z,
        ).grid(row=0, column=3, sticky="ew", padx=15, pady=5)
        self.entry_z = entry_z
        self.max_value = ttk.StringVar(value=f"Max: {self.z_max}")
        ttk.Label(frame_visual, textvariable=self.max_value, style="Custom.TLabel").grid(
            row=0, column=4, sticky="w", padx=5, pady=5
        )
        # ----------------------buttons----------------------
        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_buttons.columnconfigure(0, weight=1)
        create_buttons(
            self.frame_buttons,
            callback_sliceFile=self.slice_geometry,
            callback_saveSettings=self.print_file_callback,
        )
        print("init slice file")

    def check_parameter_settings(self, settings=None):
        settings = read_settings() if settings is None else settings
        param_list = [
            "rotation",
            "scale",
            "translation",
            "hatcher_type",
            "hatch_angle",
            "volume_offset_hatch",
            "spot_compensation",
            "num_inner_contours",
            "num_outer_contours",
            "hatch_spacing",
            "stripe_width",
            "projector_dimension",
            "projector_resolution",
            "projector_offset",
            "dpi",
            "layer_depth",
            "delta_layer",
            "plate",
        ]
        status_frames = settings.get("status_frames", [0, 0, 0, 0])
        status_frames[2] = 1
        for param in param_list:
            if param not in settings.keys():
                status_frames[2] = 0
                break
        self.callbacks["change_tab_text"](status_frames, "from init slice")
        update_settings(status_frames=status_frames)

    def print_file_callback(self):
        if self.display_thread is not None:
            # kill the thread
            self.display_thread.join()
        # ---------------------retrieve parameters--------------------
        rotation, scale, translation = get_geometry_parameters(self.entries)
        (
            hatcher_type,
            hatch_angle,
            volume_offset,
            spot_compensation,
            inner_contours,
            outer_contours,
            hatch_spacing,
            stripe_width,
        ) = get_hatching_parameters(self.entries)
        # ---------------------update parameters--------------------
        update_settings(
            rotation=rotation,
            scale=scale,
            translation=translation,
            hatcher_type=hatcher_type,
            hatch_angle=hatch_angle,
            volume_offset_hatch=volume_offset,
            spot_compensation=spot_compensation,
            num_inner_contours=inner_contours,
            num_outer_contours=outer_contours,
            hatch_spacing=hatch_spacing,
            stripe_width=stripe_width,
        )
        settings = read_settings()
        status_frames = settings.get("status_frames")
        status_frames[2] = 1
        self.callbacks["change_tab_text"](status_frames, "from slice print file")

    def scale_callback(self, value):
        value = float(value)
        if self.z_value != value:
            self.z_value = round(value, 3)
            self.entry_z.set(self.z_value)
            self.slice_geometry()

    def slice_geometry(self):
        try:
            settings = read_settings()
            rotation, scale, translation = get_geometry_parameters(self.entries)
            solid_part = read_stl_frame(
                file_path=settings.get("filepath"),
                rotation=rotation,
                scale=rotation,
                translation=translation,
            )
            if solid_part is None:
                return None
            (
                hatcher_type,
                hatch_angle,
                volume_offset_hatch,
                spot_compensation,
                num_inner_contours,
                num_outer_contours,
                hatch_spacing,
                stripe_width,
            ) = get_hatching_parameters(self.entries)
            update_settings(
                hatcher_type=hatcher_type,
                hatch_angle=hatch_angle,
                volume_offset_hatch=volume_offset_hatch,
                spot_compensation=spot_compensation,
                num_inner_contours=num_inner_contours,
                num_outer_contours=num_outer_contours,
                hatch_spacing=hatch_spacing,
                stripe_width=stripe_width,
            )
            current_z = float(self.entry_z.get())
            if not (0 < current_z < self.z_max):
                msg = "z value out of range"
                messagebox.showerror("Error", msg)
                return None
            # print("slicing: ", settings.get("filepath"), " at z=", current_z)
            my_hatcher = build_hatcher(
                hatcher_type=hatcher_type,
                hatch_angle=hatch_angle,
                volume_offset_hatch=volume_offset_hatch,
                spot_compensation=spot_compensation,
                num_inner_contours=num_inner_contours,
                num_outer_contours=num_outer_contours,
                hatch_spacing=hatch_spacing,
                stripe_width=stripe_width,
            )
            # Slice the object at Z and get the boundaries
            geom_slice = solid_part.getVectorSlice(current_z, simplificationFactor=0.9, simplificationFactorMode="absolute", simplificationPreserveTopology=True)
            # print("slicing: ", settings.get("filepath"), " at z=", current_z)
            # Perform the hatching operations
            layer = my_hatcher.hatch(geom_slice)
            dpi = settings.get("dpi")
            if self.plotter is None:
                self.plotter = PlotSTL(
                    self,
                    layer=None,
                    type_plot="layer",
                    dpi=200,
                    save_temp_flag=True,
                    path_to_save="files/img/temp.png",
                )
            projector_dimension = settings.get("projector_dimension")
            centroide = settings.get("centroide", [0, 0, 0])
            width = settings.get("width_part", 0.0)
            height = settings.get("height_part", 0.0)
            self.plotter.plotLayer(
                200,
                layer,
                projector_dimension[0],
                projector_dimension[1],
                "files/img/temp.png",
                centroide,
                width,
                height,
                clean_plot=True,
                contour_coords=geom_slice
            )
            self.canvas_img.reaload_image()
            return layer
        except Exception as e:
            print("error at internal slicing: ", e)
            return None
