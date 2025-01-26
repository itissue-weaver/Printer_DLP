# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 26/ene/2025  at 15:26 $"

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
)
from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture
from OpenGL.raw.GL.VERSION.GL_4_0 import GL_QUADS
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from pygame import OPENGL, DOUBLEBUF, FULLSCREEN

# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
from Dlp4710 import Dlp4710 as dlp4710

mode = 60
dlp = None


def load_texture(image_path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = pygame.image.load(image_path)
    image = pygame.transform.flip(image, False, True)  # Flip the image vertically
    image_data = pygame.image.tostring(image, "RGBA", 1)
    width, height = image.get_rect().size
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


try:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), OPENGL | DOUBLEBUF | FULLSCREEN)
    W, H = screen.get_size()
    width = 1.0
    height = (float(H) / W) * width
    glMatrixMode(GL_PROJECTION)
    glOrtho(-width / 2, +width / 2, -height / 2, +height / 2, -height / 2, +height / 2)
    glMatrixMode(GL_MODELVIEW)

    texture = load_texture("pyramid_test.png")

    dlp = dlp4710(mode, change_mode=False)

    while True:
        dlp.clear()
        glPushMatrix()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

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

        dlp.show()
finally:
    pygame.quit()
    dlp.cleanup() if dlp is not None else None
