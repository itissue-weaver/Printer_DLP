# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 19/1/2025  at 15:00 $'


import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Dlp4710 import Dlp4710 as dlp4710
mode = 60
size = 0.025
amplitude = 0.2
frequency = 2.0
dlp = None
try:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), OPENGL | DOUBLEBUF | FULLSCREEN)
    W, H = screen.get_size()
    width = 1.0
    height = (float(H)/W)*width
    glMatrixMode(GL_PROJECTION)
    glOrtho(-width/2, +width/2, -height/2, +height/2, -height/2, +height/2)
    glMatrixMode(GL_MODELVIEW)
    quad = gluNewQuadric()

    dlp = dlp4710(mode, change_mode=False)
    ifi = 1.0/mode

    time = 0
    while True:
        dlp.clear()
        glPushMatrix()
        ang = 2*math.pi*frequency*time
        glTranslated(amplitude*math.cos(ang), amplitude*math.sin(ang), 0)
        gluDisk(quad, 0, size, 100, 1)
        glPopMatrix()
        dlp.show()
        time += ifi
finally:
    dlp.cleanup() if dlp is not None else None
    pygame.quit()
