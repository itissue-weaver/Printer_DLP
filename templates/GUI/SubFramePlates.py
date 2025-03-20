# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/mar/2025  at 11:23 $"

import ttkbootstrap as ttk
from PIL import Image, ImageDraw, ImageTk

from files.constants import image_path_plates


class FrameImage(ttk.Frame):
    def __init__(self, master, texts=None, colors_rect=None):
        super().__init__(master)
        alpha_b = 50
        self.colors_rect = [(155, 155, 0, alpha_b), (255, 0, 0, alpha_b), (0, 255, 0, alpha_b), (0, 0, 255, alpha_b)] if colors_rect is None else colors_rect
        self.texts = ["Select Material", "Select Material", "Select Material", "Select Material"] if texts is None else texts
        self.master = master
        self.text_ids = []
        self.create_widgets()

    def create_widgets(self):
        original_image = Image.open(image_path_plates)
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
        x0_0 = width * 1 / 4 - width_rect / 2 + offset_2[0]
        y0_0 = height * 1 / 4 - height_rect / 2 + offset_2[1]
        x1_0 = width * 1 / 4 - width_rect / 2 + width_rect + offset_2[0]
        y1_0 = height * 1 / 4 - height_rect / 2 + height_rect + offset_2[1]
        draw.rectangle(
            [(x0_0, y0_0), (x1_0, y1_0)],
            fill=self.colors_rect[0]
        )
        offset_3 = (40.0, -150.0)
        x0_1 = width * 1 / 4 - width_rect / 2 + offset_3[0]
        y0_1 = height * 3 / 4 - height_rect / 2 + offset_3[1]
        x1_1 = width * 1 / 4 - width_rect / 2 + width_rect + offset_3[0]
        y1_1 = height * 3 / 4 - height_rect / 2 + height_rect + offset_3[1]
        draw.rectangle(
            [(x0_1, y0_1), (x1_1, y1_1)],
            fill=self.colors_rect[1]
        )
        offset_4 = (-45.0, -20.0)
        x0_2 = width * 3 / 4 - width_rect / 2 + offset_4[0]
        y0_2 = height * 1 / 4 - height_rect / 2 + offset_4[1]
        x1_2 = width * 3 / 4 - width_rect / 2 + width_rect + offset_4[0]
        y1_2 = height * 1 / 4 - height_rect / 2 + height_rect + offset_4[1]
        draw.rectangle(
            [(x0_2, y0_2), (x1_2, y1_2)],
            fill=self.colors_rect[2]
        )
        offset_1 = (-45.0, -150.0)
        x0_3 = width * 3 / 4 - width_rect / 2 + offset_1[0]
        y0_3 = height * 3 / 4 - height_rect / 2 + offset_1[1]
        x1_3 = width * 3 / 4 - width_rect / 2 + width_rect + offset_1[0]
        y1_3 = height * 3 / 4 - height_rect / 2 + height_rect + offset_1[1]
        draw.rectangle(
            [(x0_3, y0_3), (x1_3, y1_3)],
            fill=self.colors_rect[3]
        )
        self.overlay_image = ImageTk.PhotoImage(overlay)
        self.canvas.create_image(0, 0, anchor="nw", image=self.overlay_image)

        text_id1 = self.canvas.create_text(x0_0, y0_0, text=self.texts[0], font=("Arial", 16), fill="BLACK")
        text_id2 = self.canvas.create_text(x0_1, y0_1, text=self.texts[1], font=("Arial", 16), fill="BLACK")
        text_id3 = self.canvas.create_text(x0_2, y0_2, text=self.texts[2], font=("Arial", 16), fill="BLACK")
        text_id4 = self.canvas.create_text(x0_3, y0_3, text=self.texts[3], font=("Arial", 16), fill="BLACK")
        self.text_ids = [text_id1, text_id2, text_id3, text_id4]
        # self.button = ttk.Button(self, text="Botón de Prueba")
        # self.canvas.create_window(150, 200, window=self.button)

    def change_texts(self, texts):
        for text_id, text in zip(self.text_ids, texts):
            self.canvas.itemconfig(text_id, text=text)