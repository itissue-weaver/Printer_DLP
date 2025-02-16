# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 12/feb/2025  at 21:08 $"

from files.constants import image_path_projector


class PrinterHandle:
    def __init__(self, **kwargs):
        self.image_path = kwargs.get("image_path", image_path_projector)

    def change_image_procedure(self):
        pass
