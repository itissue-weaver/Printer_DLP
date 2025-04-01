# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:03 $"


import ttkbootstrap as ttk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyslm.visualise
from PIL import Image, ImageTk

from files.constants import image_path_projector
from templates.AuxiliarHatcher import divide_solid_in_z_parts


class PlotSTL(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.type_plot = kwargs.get("type_plot", "mesh_3d")
        self.save_temp_flag = kwargs.get("save_temp_flag", False)
        self.path_to_save = kwargs.get("path_to_save", image_path_projector)
        self.dpi = kwargs.get("dpi", 300)
        self.figure = Figure(figsize=(5, 5), dpi=self.dpi)
        self.axes = self.figure.add_subplot(111)
        match self.type_plot:
            case "mesh_3d":
                solid_trimesh_part = kwargs.get("solid_trimesh_part")
                self.figure = Figure(figsize=(5, 5), dpi=150)
                self.axes = self.figure.add_subplot(111, projection="3d")
                self.canvas = FigureCanvasTkAgg(self.figure, self)
                toolbar = NavigationToolbar2Tk(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)
                if solid_trimesh_part is not None:
                    self.axes.plot_trisurf(
                        solid_trimesh_part.vertices[:, 0],
                        solid_trimesh_part.vertices[:, 1],
                        triangles=solid_trimesh_part.faces,
                        Z=solid_trimesh_part.vertices[:, 2],
                        cmap="viridis",
                    )
                    self.axes.set_xlabel("X")
                    self.axes.set_ylabel("Y")
                    self.axes.set_zlabel("Z")
                    self.axes.set_title("3D Part")

    def plotLayer(
        self,
        dpi,
        layer,
        projector_width_cm,
        projector_height_cm,
        path_to_save,
        centroide,
        width,
        height,
        clean_plot=False,
    ):
        if layer is None:
            print("No layer found")
            return
        if width == 0.0 or height == 0.0:
            print("No width or height found")
            return
        if clean_plot:
            self.axes.clear()
            # self.figure.clf()
        pyslm.visualise.plot(
            layer,
            plot3D=False,
            plotOrderLine=False,
            plotArrows=False,
            handle=(self.figure, self.axes),
        )
        self.axes.set_xlim(
            [centroide[0] - width * 1.5 / 2, centroide[0] + width * 1.5 / 2]
        )
        self.axes.set_ylim(
            [centroide[1] - height * 1.5 / 2, centroide[1] + height * 1.5 / 2]
        )
        self.axes.set_axis_off()
        if self.save_temp_flag:
            # Convert cm to inches (1 inch = 2.54 cm)
            width_inch = projector_width_cm / 2.54
            height_inch = projector_height_cm / 2.54
            # Set the figure size
            self.figure.set_size_inches(width_inch, height_inch)
            # Set the background color of the figure and axes to black
            self.figure.patch.set_facecolor("black")
            self.figure.gca().patch.set_facecolor("black")
            self.figure.gca().tick_params(
                colors="white"
            )  # Optional: Set the tick color to white for better visibility
            # Turn off the axes
            self.figure.gca().axis("off")
            # Save the figure without axes lines at 1:1 scale
            self.figure.savefig(
                path_to_save,
                bbox_inches="tight",
                pad_inches=0,
                dpi=dpi,
                transparent=True,
            )
        else:
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)


class SolidViewer(ttk.Frame):
    def __init__(self, parent, solid_trimesh_part, parts, **kwargs):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 10), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.parts = parts
        self.solid = solid_trimesh_part
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.plot_solid()

    def plot_solid(self):
        subsolids = divide_solid_in_z_parts(self.solid, self.parts)
        colors = ["black", "blue", "yellow", "red"]

        for subsolid, color in zip(subsolids, colors):
            self.ax.plot_trisurf(
                subsolid.vertices[:, 0],
                subsolid.vertices[:, 1],
                triangles=subsolid.faces,
                Z=subsolid.vertices[:, 2],
                color=color,
            )
        self.ax.set_axis_off()
        self.ax.set_title("3D Part")

    def change_solid(self, solid_trimesh_part):
        self.ax.clear()
        self.solid = solid_trimesh_part
        self.plot_solid()
        # self.canvas.draw()

    def change_parts(self, parts):
        self.ax.clear()
        self.parts = parts
        self.plot_solid()


class ImageFrameApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = None
        self.image = None
        self.image_start = None
        self.load_image()
        self.create_widgets()

    def load_image(self):
        try:
            self.image = Image.open(r"files/img/temp.png")
        except Exception as e:
            print(f"Error loading image: {e}")

    def create_widgets(self):
        self.canvas = ttk.Canvas(self.master)
        self.canvas.grid(row=0, column=0, sticky="n")
        if self.image is not None:
            self.show_image()

    def show_image(self):
        width, height = self.image.size
        new_width = int(width / 2.5)
        new_height = int(height / 2.5)
        resized_image = self.image.resize((new_width, new_height))
        self.image_start = ImageTk.PhotoImage(resized_image)
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_start)

    def reaload_image(self):
        self.load_image()
        self.show_image()
