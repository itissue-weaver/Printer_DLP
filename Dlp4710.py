# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 19/ene/2025  at 15:16 $"
import subprocess
import time

import pygame
from OpenGL.GL import *
from pygame.locals import *

'''
Helper class for using the DLP4710 (written by Mark Wexler, public domain)
Keeps track of colors, bits, clears, flips in both 180 and 1440 Hz modes

Class constructor parameters:
mode: 60, 180, or 1440
mode_color: 'R', 'G', 'B' (for 180 or 1440 mode) or 'RGB' (for 1440);
            or None to use default values (defined in default_parameters)
            (default: None)
mode_timings: list of pre-frame, frame, and post-frame durations in microseconds
              or None to use default values (defined in default_parameters)
              (default: None)
change_mode: whether to change projector mode automatically using the external
             dlpmode program (default: True)

If change_mode is true, then you must:
- install the dlpmode.exe program and any required DLLs
- set the dlpmode_exe global variable (below) to the absolute or relative
  path of dlpmode.exe

Typical use (1440 Hz):

import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import dlp4710

mode = 1440
size = 0.025
amplitude = 0.2
frequency = 2.0

try:
    pygame.init()
    screen = pygame.display.set_mode((0,0), OPENGL|DOUBLEBUF|FULLSCREEN)
    W, H = screen.get_size()
    width = 1.0
    height = (float(H)/W)*width
    glMatrixMode(GL_PROJECTION)
    glOrtho(-width/2, +width/2, -height/2, +height/2, -height/2, +height/2)
    glMatrixMode(GL_MODELVIEW)
    quad = gluNewQuadric()

    dlp = dlp4710.dlp4710(mode)
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
    dlp.cleanup()
    pygame.quit()
'''



modes = (60, 180, 1440)
default_parameters = {
    180: {'color': 'G', 'timings': [350, 5000, 206]},
    1440: {'color': 'G', 'timings': [193, 451, 50]}}
dlpmode_exe = r'dlpmode.exe'


# color can be 'R', 'G', 'B', or 'RGB'; or 0, 1, 2
def set_mode(freq, color=None, timings=None):
    if freq not in modes:
        raise ValueError
    if freq != 60:
        if color is None:
            color = default_parameters[freq]['color']
        if timings is None:
            timings = default_parameters[freq]['timings']
        if type(color) is int:
            if 0 <= color <= 2:
                color = ['R', 'G', 'B'][color]
            else:
                raise ValueError
        if color.upper() not in ('R', 'G', 'B', 'RGB'):
            raise ValueError
    cmd = dlpmode_exe
    cmd += ' ' + str(freq)
    if freq != 60:
        cmd += ' ' + color
        if timings is not None:
            try:
                z = ' '.join(map(str, map(int, timings)))
            except Exception as e:
                print(e)
                raise ValueError
            if len(timings) != 3:
                raise ValueError
            cmd += ' ' + z
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # the reason I'm blanking the environment variables in the shell escape
    # below is a weird error: if the PATH variable is above a certain length,
    # then the communications calls fail for some mysterious reason
    # out = subprocess.check_output(cmd, env = {}, startupinfo = si)
    out = subprocess.check_output(cmd, startupinfo=si)
    return out


class Dlp4710:

    def __init__(self, mode=1440, mode_color=None, mode_timings=None,
                 change_mode=True):
        if mode not in modes:
            raise ValueError
        self.mode = mode
        self.change_mode = change_mode
        if self.change_mode:
            set_mode(self.mode, mode_color, mode_timings)
        glPushAttrib(GL_ENABLE_BIT)
        if self.mode == 180:
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        elif self.mode == 1440:
            glEnable(GL_COLOR_LOGIC_OP)
            glLogicOp(GL_COPY)
            '''
            glEnable(GL_BLEND)
            glBlendFunc(GL_ONE, GL_ZERO)
            '''
        self.n = 0
        self.max_n = int(round(self.mode / 60))
        self.frame_dur_sum = 0
        self.frame_dur_n = 0
        self.last_t = None

    def cleanup(self):
        if self.change_mode:
            set_mode(60)

    # def clear(self):
    #     if self.n == 0:
    #         t = time.process_time()
    #         if self.last_t is not None:
    #             frame_dur = t - self.last_t
    #             self.frame_dur_sum += frame_dur
    #             self.frame_dur_n += 1
    #         self.last_t = t
    #         if self.mode == 180:
    #             glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    #         elif self.mode == 1440:
    #             glLogicOp(GL_COPY)
    #             # glBlendFunc(GL_ONE, GL_ZERO)
    #         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#
    #     if self.mode == 180:
    #         # in mode 180, always use grays: glColor(g, g, g)
    #         if self.n == 0:
    #             glColorMask(GL_FALSE, GL_FALSE, GL_TRUE, GL_TRUE)
    #         elif self.n == 1:
    #             glColorMask(GL_FALSE, GL_TRUE, GL_FALSE, GL_TRUE)
    #         elif self.n == 2:
    #             glColorMask(GL_TRUE, GL_FALSE, GL_FALSE, GL_TRUE)
    #     elif self.mode == 1440:
    #         # set the color; when drawing in mode 1440, DON'T CHANGE COLOR
    #         glLogicOp(GL_OR)
    #         # glBlendFunc(GL_ONE, GL_ONE)
    #         c = 2 - self.n // 8
    #         d = self.n % 8
    #         col = 3 * [0]
    #         col[c] = 1 << d
    #         glColor3ubv(col)

    def clear(self):
        if self.n == 0:
            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE,
                        GL_TRUE)  # Ensure color mask is set to allow writing to all color channels
            glClearColor(0.0, 0.0, 0.0, 1.0)  # Ensure clear color is black
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            t = time.process_time()
            if self.last_t is not None:
                frame_dur = t - self.last_t
                self.frame_dur_sum += frame_dur
                self.frame_dur_n += 1
            self.last_t = t
            if self.mode == 180:
                glColorMask(GL_FALSE, GL_FALSE, GL_TRUE, GL_TRUE)
            elif self.mode == 1440:
                glLogicOp(GL_COPY)

        if self.mode == 180:
            if self.n == 0:
                glColorMask(GL_FALSE, GL_FALSE, GL_TRUE, GL_TRUE)
            elif self.n == 1:
                glColorMask(GL_FALSE, GL_TRUE, GL_FALSE, GL_TRUE)
            elif self.n == 2:
                glColorMask(GL_TRUE, GL_FALSE, GL_FALSE, GL_TRUE)
        elif self.mode == 1440:
            glLogicOp(GL_OR)
            c = 2 - self.n // 8
            d = self.n % 8
            col = 3 * [0]
            col[c] = 1 << d
            glColor3ubv(col)

    def show(self, return_events=True, check_quit=True):
        self.n = (self.n + 1) % self.max_n
        if self.n == 0:
            pygame.display.flip()
        if return_events:
            events = pygame.event.get()
            for e in events:
                if check_quit:
                    if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                        raise KeyboardInterrupt()
            return events

    def frame_rate(self):
        return self.mode

    def frame_rate_measured(self):
        if self.frame_dur_n == 0:
            return None
        return self.frame_dur_n / self.frame_dur_sum

    def subframe(self):
        return self.n % self.max_n

    def reset(self):
        self.n = 0

    def flush(self):
        events = []
        while self.n != 0:
            self.clear()
            events += self.show()
        return events
