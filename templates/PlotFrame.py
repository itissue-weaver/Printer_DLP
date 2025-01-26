# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:03 $"

import matplotlib
import ttkbootstrap as ttk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyslm.visualise


class PlotSTL(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.type_plot = kwargs.get("type_plot", "mesh_3d")
        self.save_temp_flag = kwargs.get("save_temp_flag", False)
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
            case "layer":
                layer = kwargs.get("layer")
                if layer is None:
                    return
                self.dpi = kwargs.get("dpi", 300)  # Adjust as needed to achieve the scale

                matplotlib.pyplot.close("all")
                self.figure = Figure(figsize=(5, 5), dpi=self.dpi)
                self.axes = self.figure.add_subplot(111)
                self.figure, self.axes = pyslm.visualise.plot(
                    layer,
                    plot3D=False,
                    plotOrderLine=True,
                    plotArrows=False,
                )
                if self.save_temp_flag:
                    # projector_width_cm = 15.0  # Width of the projected image at a 10 cm distance
                    # projector_height_cm = 10.0  # Height of the projected image at a 10 cm distance
                    projector_width_cm = kwargs.get("projector_width_cm", 10.0)
                    projector_height_cm = kwargs.get("projector_height_cm", 10.0)
                    # Convert cm to inches (1 inch = 2.54 cm)
                    width_inch = projector_width_cm / 2.54
                    height_inch = projector_height_cm / 2.54
                    # Set the figure size
                    self.figure.set_size_inches(width_inch, height_inch)

                    # Set the background color of the figure and axes to black
                    self.figure.patch.set_facecolor('black')
                    self.figure.gca().patch.set_facecolor('black')
                    self.figure.gca().tick_params(
                        colors='white')  # Optional: Set the tick color to white for better visibility
                    # Turn off the axes
                    self.figure.gca().axis('off')
                    # Save the figure without axes lines at 1:1 scale
                    self.figure.savefig("temp.png", bbox_inches="tight", pad_inches=0,
                                        dpi=self.dpi, transparent=True)
                else:
                    self.canvas = FigureCanvasTkAgg(self.figure, self)
                    toolbar = NavigationToolbar2Tk(self.canvas, self)
                    toolbar.update()
                    self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)
            case _:
                print("No type plot")
