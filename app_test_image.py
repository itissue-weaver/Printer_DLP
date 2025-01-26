# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 26/ene/2025  at 15:49 $"

import pygame
from OpenGL.GL import glGenTextures, glTexImage2D, glBegin, glEnd
from OpenGL.raw.GL.ARB.internalformat_query2 import GL_TEXTURE_2D
from OpenGL.raw.GL.VERSION.GL_1_0 import (
    GL_RGBA,
    glTexParameteri,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    glMatrixMode,
    GL_PROJECTION,
    glOrtho,
    GL_MODELVIEW,
    glPushMatrix,
    glEnable,
    glTexCoord2f,
    glVertex2f,
    glDisable,
    glPopMatrix,
    glClearColor,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_BLEND,
    glBlendFunc,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
)
from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture
from OpenGL.raw.GL.VERSION.GL_4_0 import GL_QUADS
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from pygame import OPENGL, DOUBLEBUF, FULLSCREEN
from Dlp4710 import Dlp4710 as dlp4710


class DlpViewer:
    def __init__(self, mode=60, image_path="temp.png"):
        self.mode = mode
        self.image_path = image_path
        self.dlp = None
        self.texture = None

    def load_texture(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        try:
            # image = pygame.image.load(self.image_path)
            image = pygame.image.load(self.image_path).convert_alpha()
            if not image:
                raise ValueError("Image could not be loaded.")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            raise

        # Image Transformations
        image = pygame.transform.flip(image, False, True)  # Flip the image vertically
        image_data = pygame.image.tostring(image, "RGBA", True)
        width, height = image.get_rect().size

        # Creating/OpenGL texture
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data,
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture

    def init_display(self):
        pygame.init()
        screen = pygame.display.set_mode((0, 0), OPENGL | DOUBLEBUF | FULLSCREEN)
        W, H = screen.get_size()
        width = 1.0
        height = (float(H) / W) * width
        glMatrixMode(GL_PROJECTION)
        glOrtho(
            -width / 2, +width / 2, -height / 2, +height / 2, -height / 2, +height / 2
        )
        glMatrixMode(GL_MODELVIEW)

        # Ensure depth test is disabled
        glDisable(GL_DEPTH_TEST)

        self.texture = self.load_texture()
        self.dlp = dlp4710(self.mode, change_mode=False)

    def display_image(self):
        try:
            self.init_display()
            # Enable blending and set the blend function
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.cleanup()
                        return

                self.dlp.clear()
                glClearColor(0.0, 0.0, 0.0, 1.0)  # Set the clear color to black
                glClear(GL_COLOR_BUFFER_BIT)  # Ensure we clear the screen properly

                glPushMatrix()
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture)

                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(-0.1, -0.1)
                glTexCoord2f(1, 0)
                glVertex2f(+0.1, -0.1)
                glTexCoord2f(1, 1)
                glVertex2f(+0.1, +0.1)
                glTexCoord2f(0, 1)
                glVertex2f(-0.1, +0.1)
                glEnd()

                glDisable(GL_TEXTURE_2D)
                glPopMatrix()

                pygame.display.flip()
                self.dlp.show()

        finally:
            self.cleanup()

    def cleanup(self):
        if self.dlp is not None:
            self.dlp.cleanup()
        pygame.quit()


# To call the class (example):
viewer = DlpViewer()
viewer.display_image()
