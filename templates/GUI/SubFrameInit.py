# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/mar/2025  at 19:24 $"

import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageSequence  # For GIF processing

from files.constants import gif_path  # Ensure this is the path to your GIF file


class GifFrameApp(ttk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Starting GIF")
        self.attributes("-topmost", True)
        self.attributes("-fullscreen", True)
        self.overrideredirect(True)  # Remove window decorations for a cleaner display
        self.configure(
            background="white"
        )  # Set background to white to fix transparency issues

        # Create a canvas for displaying the GIF
        gif_canvas = ttk.Canvas(self, highlightthickness=0, background="white")
        gif_canvas.pack(fill="both", expand=True)

        # Load and process the GIF
        gif = Image.open(gif_path)  # Replace with the path to your GIF
        frames = []

        # Flatten transparency of the GIF to a white background
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")  # Ensure RGBA mode
            background = Image.new(
                "RGBA", frame.size, (255, 255, 255)
            )  # White background
            merged = Image.alpha_composite(
                background, frame
            )  # Merge background and frame
            frames.append(
                ImageTk.PhotoImage(merged.convert("RGB"))
            )  # Convert back to RGB

        # Get screen width and height for centering
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        image_width, image_height = (
            frames[0].width(),
            frames[0].height(),
        )  # Assume all frames have the same size

        x_center = (screen_width - image_width) // 2
        y_center = (screen_height - image_height) // 2

        # Function to animate the GIF on the canvas
        def update_frame(idx=0):
            if idx < len(frames):
                gif_canvas.delete("all")  # Clear previous frame to avoid stacking
                gif_canvas.create_image(
                    x_center, y_center, anchor="nw", image=frames[idx]
                )
                self.after(100, update_frame, idx + 1)  # Adjust frame rate
            else:
                self.after(100, update_frame, 0)  # Loop the animation

        update_frame()

        # Automatically close the Toplevel after 6 seconds
        self.after(6000, self.destroy)
        print("GIF closed")