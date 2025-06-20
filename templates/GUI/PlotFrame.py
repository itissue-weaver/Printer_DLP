# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:03 $"


import ttkbootstrap as ttk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyslm.visualise
from PIL import Image, ImageTk
from matplotlib.patches import Polygon

from files.constants import image_path_projector, path_solid_capture, desired_width_slice_image
from templates.AuxFunctionsPlots import postprocessor_image, hatch_for_plot
from templates.AuxiliarHatcher import divide_solid_in_z_parts


class PlotSTL(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.type_plot = kwargs.get("type_plot", "mesh_3d")
        self.save_temp_flag = kwargs.get("save_temp_flag", False)
        self.path_to_save = kwargs.get("path_to_save", image_path_projector)
        self.callbacks = kwargs.get("callbacks", {})
        self.dpi = kwargs.get("dpi", 300)
        self._from = kwargs.get("_from", "FrameSlice")
        self.figure = Figure(figsize=(5, 5), dpi=self.dpi)
        self.axes = self.figure.add_subplot(111)
        match self.type_plot:
            case "mesh_3d":
                solid_trimesh_part = kwargs.get("solid_trimesh_part")
                solid_part = kwargs.get("solid_part")
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
                        solid_trimesh_part.vertices[:, 2],  # <- aquí va Z como argumento posicional
                        triangles=solid_trimesh_part.faces,
                        cmap="viridis",
                    )
                    self.axes.set_xlabel("X")
                    self.axes.set_ylabel("Y")
                    self.axes.set_zlabel("Z")
                    # self.axes.set_title("3D Part")
                if self._from == "FramePrinting":
                    self.axes.set_axis_off()
                    self.save_capture()

    def save_capture(self, filename=path_solid_capture):
        self.figure.savefig(filename, dpi=300, bbox_inches='tight')
        self.callbacks.get("render_thumbnails")()

    def plot_layer(
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
        contour_coords=None,
        is_final=True
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
            (centroide[0] - width * 1.25 / 2, centroide[0] + width * 1.25 / 2)
        )
        self.axes.set_ylim(
            (centroide[1] - height * 1.25 / 2, centroide[1] + height * 1.25 / 2)
        )
        for line in self.axes.get_lines():
            line.set_color("white")
        # if contour_coords is not None:
        #     count=0
        #     for contour in contour_coords:
        #         # contour[:, 0] = contour[:, 0] - centroide[0] + width / 2
        #         # contour[:, 1] = contour[:, 1] - centroide[1] + height / 2
        #         # contour[:, 0] *= desired_width_slice_image / width
        #         # contour[:, 1] *= desired_width_slice_image / height
        #         white_fill = Polygon(contour, closed=True, facecolor="white", edgecolor="white")
        #         self.axes.add_patch(white_fill)
        #         count+=1
        #         print(count)

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
            res = postprocessor_image(path_to_save, is_final)
            if not res:
                print("Error saving image")
        else:
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)


class SolidViewer(ttk.Frame):
    def __init__(self, parent, solid_trimesh_part, parts, **kwargs):
        super().__init__(parent)
        self.figure = Figure(figsize=(10, 10), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.callbacks = kwargs.get("callbacks", {})
        self.parts = parts
        self.solid = solid_trimesh_part
        self.layer_thickness = kwargs.get("layer_thickness", 0.5)
        self.solid_part = kwargs.get("solid_part", None)
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.plot_solid(self.solid_part)

    def plot_solid(self, solid_part):
        import numpy as np
        from matplotlib import cm

        self.ax.clear()
        layers = hatch_for_plot(solid_part, self.layer_thickness)
        num_blocks = self.parts
        n = 4
        total_layers = len(layers)
        layers_per_block = total_layers // num_blocks
        colors = ['red', 'green', 'blue', 'orange']
        for i in range(0, len(layers), n):  # n es el salto entre capas
            layer = layers[i]
            z = float(layer.z) / 1000.0
            block_idx = min(i // layers_per_block, num_blocks - 1)
            color = colors[block_idx]
            # Extraemos hatches como coordenadas
            sampling_rate = 5  # Muestra 1 de cada 7 segmentos
            for hatch_geom in layer.getHatchGeometry():
                coords = np.array(hatch_geom.coords).reshape(-1, 2, 2)
                coords = coords[::sampling_rate]  # Submuestreo

                for seg in coords:
                    x = [seg[0][0], seg[1][0]]
                    y = [seg[0][1], seg[1][1]]
                    self.ax.plot(x, y, zs=z, zdir='z', color=color, linewidth=0.5)
                    self.ax.view_init(elev=15, azim=0)  # Vista desde arriba
        self.canvas.draw()
        self.ax.set_axis_off()
        self.save_image()


    def save_image(self, filename=path_solid_capture):
        self.figure.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Imagen guardada como {filename}")
        self.callbacks["render_thumbnails"]()

class ImageFrameApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = None
        self.image = None
        self.image_start = None
        self.load_image()
        # print("image loaded")
        self.create_widgets()

    def load_image(self, filepath=r"files/img/temp.png"):
        try:
            self.image = Image.open(filepath)
        except Exception as e:
            print(f"Error loading image: {e}")

    def create_widgets(self):
        self.canvas = ttk.Canvas(self.master)
        self.canvas.grid(row=0, column=0, sticky="n")
        # print("canvas created")
        if self.image is not None:
            self.show_image()

    def show_image(self):
        width, height = self.image.size
        desired_width = desired_width_slice_image
        factor = desired_width / width
        new_height = int(height * factor)
        # resized_image = self.image.resize((desired_width, new_height))
        resized_image = self.image.resize((desired_width, new_height)).convert("RGB")
        # print("image resized",  desired_width, new_height)
        self.image_start = ImageTk.PhotoImage(resized_image)
        # print("image resized")
        self.canvas.config(width=desired_width, height=new_height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_start)

    def reload_image(self):
        self.load_image()
        self.show_image()

    def reload_clean_image(self):
        self.load_image(r"files/img/black_screen.png")
        self.show_image()