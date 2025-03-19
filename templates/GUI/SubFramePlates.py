# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/mar/2025  at 11:23 $"

import ttkbootstrap as ttk
from PIL import Image, ImageDraw, ImageTk

class FrameImagePlate(ttk.Frame):
    def __init__(self, master, texts=None, colors_rect=None):
        super().__init__(master)
        alpha = 50
        self.colors_rect = [(255, 0, 0, alpha), (0, 255, 0, alpha), (0, 0, 255, alpha), (155, 155, 0, alpha), ] if colors_rect is None else colors_rect
        self.texts = ["Text1", "Text2", "Text3", "Text4"] if texts is None else texts
        self.master = master
        self.pack(fill=ttk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        original_image = Image.open("files/img/plates.png")
        scale = 0.5
        width = int(original_image.width * scale)
        height = int(original_image.height * scale)

        resized_image = original_image.resize((width, height))
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas = ttk.Canvas(self, width=self.background_image.width(), height=self.background_image.height())
        self.canvas.pack(fill=ttk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        width_rect = 120
        height_rect = 120
        overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        offset_2 = (40.0, -20.0)
        draw.rectangle(
            [
                (width * 1 / 4 - width_rect / 2 + offset_2[0], height * 1 / 4 - height_rect / 2 + offset_2[1]),
                (width * 1 / 4 - width_rect / 2 + width_rect + offset_2[0], height * 1 / 4 - height_rect / 2 + height_rect + offset_2[1])
            ],
            fill=self.colors_rect[1]
        )

        offset_3 = (40.0, -150.0)
        draw.rectangle(
            [
                (width * 1 / 4 - width_rect / 2 + offset_3[0], height * 3 / 4 - height_rect / 2 + offset_3[1]),
                (width * 1 / 4 - width_rect / 2 + width_rect + offset_3[0], height * 3 / 4 - height_rect / 2 + height_rect + offset_3[1])
            ],
            fill=self.colors_rect[2]
        )

        offset_4 = (-45.0, -20.0)
        draw.rectangle(
            [
                (width * 3 / 4 - width_rect / 2 + offset_4[0], height * 1 / 4 - height_rect / 2+ offset_4[1]),
                (width * 3 / 4 - width_rect / 2 + width_rect + offset_4[0], height * 1 / 4 - height_rect / 2 + height_rect+ offset_4[1])
            ],
            fill=self.colors_rect[3]
        )
        offset_1 = (-45.0, -150.0)
        draw.rectangle(
            [
                (width * 3 / 4 - width_rect / 2 + offset_1[0], height * 3 / 4 - height_rect / 2 + offset_1[1]),
                (width * 3 / 4 - width_rect / 2 + width_rect + offset_1[0], height * 3 / 4 - height_rect / 2 + height_rect + offset_1[1])
            ],
            fill=self.colors_rect[0]
        )
        self.overlay_image = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, anchor="nw", image=self.overlay_image)

        self.canvas.create_text(width*1/4, height*1/4, text="Texto de ejemplo", font=("Arial", 16), fill="BLACK")
        self.canvas.create_text(width*3/4, height*1/4, text="Texto de ejemplo", font=("Arial", 16), fill="BLACK")
        self.canvas.create_text(width*1/4, height*3/4, text="Texto de ejemplo", font=("Arial", 16), fill="BLACK")
        self.canvas.create_text(width*3/4, height*3/4, text="Texto de ejemplo", font=("Arial", 16), fill="BLACK")
        # self.button = ttk.Button(self, text="Botón de Prueba")
        # self.canvas.create_window(150, 200, window=self.button)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = FrameImagePlate(root)
    root.mainloop()