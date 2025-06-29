# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 26/ene/2025  at 15:49 $"

import threading
import time
from time import perf_counter, sleep

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
    GL_DEPTH_BUFFER_BIT,
    glBlendFunc,
    GL_BLEND,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
)
from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture
from OpenGL.raw.GL.VERSION.GL_4_0 import GL_QUADS
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from pygame import OPENGL, DOUBLEBUF, FULLSCREEN
from files.constants import image_path_projector, delay_z, delay_n, delay_z_lift
from templates.AuxiliarFunctions import write_log, update_flags, read_flags, read_settings
from templates.midleware.MD_Printer import (
    subprocess_control_led,
    subprocess_control_motor,
)


def turn_on_off_led(state="off"):
    try:
        thread_subprocess = threading.Thread(
            target=subprocess_control_led, args=(state,)
        )
        thread_subprocess.start()
        sleep(2)
        return True
    except Exception as e:
        print(e)
        return False


def move_motor(action, direction, location_z, motor, steps, new_delay_z, new_delay_n):
    result = subprocess_control_motor(action, direction, location_z, motor, steps, new_delay_z, new_delay_n)
    return f"Move {action}: {steps} steps, {result}\n"


def calculate_rotation_plate(new_deposit, current_deposit):
    dict_deposits = {
        "1": 0,
        "2": 90,
        "3": 180,
        "4": 270,
    }
    rotation = dict_deposits[new_deposit] - dict_deposits[current_deposit]
    if rotation < 0:
        rotation += 360
    steps = int(200 * int(rotation) / 360)
    return steps


class DlpViewer(threading.Thread):
    def __init__(self, mode=60, image_path=image_path_projector):
        super().__init__()

        self.is_error = False
        (
            self.num_layers,
            self.layer_count,
            self.layer_depth,
            self.sequence,
            self.delta_layer,
            self.delay_z_retract,
            self.delay_z_lift,
            self.delay_n,
            self.settings,
            self.dlp,
            self.texture,
            self.bottom_layers,
            self.delta_bottom,
            self.one_layer_display,
            self.lift_height,
            self.lift_height_vat,
            self.delay_retract_init,
            self.offset_x,
            self.offset_y,
            self.screen_projector_size_x,
            self.screen_projector_size_y,
        ) = (None,) * 21
        self.flag_reload = False
        self.mode = mode
        self.current_deposit_index = 0
        self.current_deposit = 1
        self.image_path = image_path
        self.running = False
        self.paused = False
        self.start_time = 0.0
        self.last_time = 0.0
        self.load_variables()

    def load_variables(self):
        self.settings = read_settings()
        self.running = False
        self.paused = False
        self.start_time = 0.0
        self.last_time = 0.0
        self.flag_reload = False
        self.delta_layer = self.settings["delta_layer"]
        self.delay_retract_init = self.settings.get("delay_retract_init", 0.01)
        self.sequence = self.settings.get("sequence", [])  # Carga la secuencia
        self.layer_depth = self.settings.get("layer_depth", 1.0)  # Espesor de la capa
        self.layer_count = 0  # Contador de capas procesadas
        self.num_layers = self.settings.get("num_layers", 0)  # Número de capas
        self.delay_z_retract = self.settings.get("delay_z", delay_z)  # Retardo de movimiento
        self.delay_z_lift = self.settings.get("delay_z_lift", delay_z_lift)  # Retardo de movimiento
        self.lift_height = self.settings.get("lift_height", 6)
        self.lift_height_vat = self.settings.get("lift_height_vat", 30)
        self.delay_n = self.settings.get("delay_n", delay_n)  # Retardo de movimiento
        self.bottom_layers = self.settings.get("b_layers", 1)
        self.delta_bottom  = self.settings.get("e_time_b_layers", 40)
        self.one_layer_display = False
        deposit = self.sequence[0] if len(self.sequence) > 0 else {}
        self.current_deposit_index = deposit.get("index", 0)
        self.current_deposit = deposit.get("deposit", 1)
        self.offset_x = self.settings.get("offset_x_screen", 0)
        self.offset_y = self.settings.get("offset_y_screen", 0)
        self.screen_projector_size_x = self.settings.get("size_projector_x", 0.1)
        self.screen_projector_size_y = self.settings.get("size_projector_y", 0.1)


    def load_texture(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        image = pygame.image.load(self.image_path).convert_alpha()
        # thread_log = threading.Thread(
        #     target=write_log, args=(f"{self.image_path} {self.layer_count}",)
        # )
        # thread_log.start()
        image = pygame.transform.flip(image, False, False)  # Flip the image vertically
        image_data = pygame.image.tostring(image, "RGBA", True)
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

    def init_display(self):
        pygame.init()
        screen = pygame.display.set_mode((0, 0), OPENGL | DOUBLEBUF | FULLSCREEN)
        w_s, h_s = screen.get_size()
        width = 1.0
        height = (float(h_s) / w_s) * width
        glMatrixMode(GL_PROJECTION)
        glOrtho(
            -width / 2, +width / 2, -height / 2, +height / 2, -height / 2, +height / 2
        )
        glMatrixMode(GL_MODELVIEW)
        self.texture = self.load_texture()
        self.layer_count += 1
        update_flags(layer_count=self.layer_count)

    def init_motors(self, delay_retract_init=None):
        r = 8 / 200
        msg = ""
        result = subprocess_control_motor(
            "move_z_sw", "ccw", "bottom", "z", 0, new_delay_z=self.delay_retract_init, new_delay_n=self.delay_n
        )
        msg += f"move z to sw {result}"
        # steps = int(self.layer_depth / r)
        # result = subprocess_control_motor(
        #     "move_z", "cw", "top", "z", steps, new_delay_z=self.delay_z_retract, new_delay_n=self.delay_n
        # )
        # msg += f"move z {result}"

    def run(self):
        try:
            self.init_motors()
            self.init_display()
            turn_on_off_led(state="on")
            flags = read_flags()
            if flags["stop_printing"]:
                self.running = False
            # Enable blending and set the blend function
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.start_time = perf_counter()
            self.last_time = perf_counter()
            self.running = True
            self.is_error = False
            error = ""
            while self.running:
                if not self.running:
                    break
                flags = read_flags()
                if flags["stop_printing"]:
                    self.running = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                if self.paused:
                    # Si está pausado, espera un momento antes de verificar de nuevo
                    time.sleep(0.1)
                    continue
                if self.one_layer_display:    # mostrar solo una capa
                    continue
                # Calcular tiempo transcurrido
                current_time = perf_counter()
                elapsed_time = current_time - self.last_time
                # Comprobar si ha pasado delta_layer
                time_to_wait = self.delta_layer if self.layer_count>self.bottom_layers else self.delta_bottom
                if elapsed_time >= time_to_wait:
                    self.layer_count += 1
                    turn_on_off_led(state="off")
                    self.change_layer_motor_sequence()
                    turn_on_off_led(state="on")
                    # thread_log = threading.Thread(
                    #     target=write_log,
                    #     args=(f"{self.layer_count}, {self.num_layers}",),
                    # )
                    # thread_log.start()
                    update_flags(layer_count= self.layer_count)
                    # print(f"{self.layer_count}, {self.num_layers}")
                    if self.layer_count > self.num_layers - 1:
                        update_flags(layer_count=0, is_complete=True)
                        self.running = False
                    self.reload_image(
                        f"files/img/extracted/temp{self.layer_count}.png"
                    )
                    self.last_time = current_time  # Resetear el temporizador
                glClearColor(0.0, 0.0, 0.0, 1.0)  # Set the clear color to black
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  #
                glPushMatrix()
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture)
                # Parámetros ajustables
                # offset_x = 0.05  # Movimiento hacia la derecha
                # offset_y = 0.05  # Movimiento hacia arriba
                # size = 0.1       # Tamaño del medio lado del cuadrado
                offset_x = self.offset_x
                offset_y = self.offset_y
                size_x = self.screen_projector_size_x
                size_y = self.screen_projector_size_y
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(-size_x + offset_x, -size_y + offset_y)

                glTexCoord2f(1, 0)
                glVertex2f(+size_x + offset_x, -size_y + offset_y)

                glTexCoord2f(1, 1)
                glVertex2f(+size_x + offset_x, +size_y + offset_y)

                glTexCoord2f(0, 1)
                glVertex2f(-size_x + offset_x, +size_y + offset_y)
                glEnd()
                # glBegin(GL_QUADS)
                # glTexCoord2f(0, 0)
                # glTexCoord2f(1, 0)
                # glVertex2f(
                #     -0.1 + offset_x, -0.1 + offset_y
                # )  # Aplicando offsets en X y Y
                #
                # glVertex2f(
                #     +0.1 + offset_x, -0.1 + offset_y
                # )  # Aplicando offsets en X y Y
                #
                # glTexCoord2f(1, 1)
                # glVertex2f(
                #     +0.1 + offset_x, +0.1 + offset_y
                # )  # Aplicando offsets en X y Y
                #
                # glTexCoord2f(0, 1)
                # glVertex2f(
                #     -0.1 + offset_x, +0.1 + offset_y
                # )  # Aplicando offsets en X y Y
                # glEnd()
                glDisable(GL_TEXTURE_2D)
                glPopMatrix()
                pygame.display.flip()

        except Exception as e:
            print(e)
            thread_log = threading.Thread(target=write_log, args=(f"Error printing: {e}",))
            thread_log.start()
            self.is_error = True
            error = str(e)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        pygame.quit()
        turn_on_off_led()
        try:
            update_flags(stop_printing=True, is_printing=False, is_error=self.is_error, error=error, layer_count=0)
        except  Exception as e:
            print(e)
            thread_log = threading.Thread(target=write_log, args=(f"Error update flags: {e}",))
            thread_log.start()

    def process_sequence(self):
        """Controla el proceso basado en la secuencia."""
        for step in self.sequence:
            target_layers = int(step["height_z"] / self.layer_depth)
            if self.layer_count == target_layers:
                print(
                    f"Procesando depósito {step['deposit']} en capa {self.layer_count}"
                )
                self.pause()
                time.sleep(2)  # Simula el tiempo muerto para reubicar depósito
                self.resume()

    def is_alive_projector(self):
        return self.running

    def change_vat(self, old_deposit, new_deposit):
        msg = ""
        r = 8 / 200  # Relación de pasos
        distance_free_vat = self.lift_height_vat-self.lift_height
        # Elevar la plataforma antes de mover lateralmente
        steps_up = int(distance_free_vat / r)
        msg += move_motor("move_z", "cw", "top", "z", steps_up, self.delay_z_lift, self.delay_n)

        steps_lateral = calculate_rotation_plate(new_deposit, old_deposit)
        # Mover lateralmente para cambiar de vat
        msg += move_motor("move_plate", "cw", "top", "plate", steps_lateral, self.delay_z_retract, self.delay_n)

        # Descender la plataforma en la nueva posición
        steps_down = int(distance_free_vat / r)
        msg += move_motor("move_z", "ccw", "bottom", "z", steps_down, self.delay_z_retract, self.delay_n)

        return msg

    def check_and_change_deposit(self, msg):
        deposit = self.sequence[self.current_deposit_index]
        current_h = self.layer_count * self.layer_depth
        if current_h >= deposit["height_z"]:
            if self.current_deposit_index+1 < len(self.sequence):
                self.current_deposit_index += 1
                new_deposit = self.sequence[self.current_deposit_index]
                self.current_deposit = new_deposit["deposit"]
                msg += self.change_vat(deposit["deposit"], self.current_deposit)
            else:
                msg += "No more deposits"
                thread_log = threading.Thread(target=write_log, args=(msg,))
                thread_log.start()
        return msg

    def change_layer_motor_sequence(self):
        r = 8 / 200  # Relación de pasos
        dist_free = self.lift_height   # altura establecida para cambiar de capa
        msg = ""

        # Elevar la plataforma según la altura establecida para cambiar de capa
        steps = int(dist_free / r)
        result = subprocess_control_motor("move_z", "cw", "top", "z", steps, new_delay_z=self.delay_z_lift, new_delay_n=self.delay_n)
        msg += f"change z motor: {steps}, {result} {dist_free} {self.layer_depth}\n"
        # thread_log = threading.Thread(target=write_log, args=(msg,))
        # thread_log.start()
        # Verificar si se alcanzó la altura de cambio de vat
        msg = self.check_and_change_deposit(msg)
        # thread_log = threading.Thread(target=write_log, args=(msg,))
        # thread_log.start()
        steps = int((dist_free - self.layer_depth) / r)
        result = subprocess_control_motor("move_z", "ccw", "top", "z", steps, new_delay_z=self.delay_z_retract, new_delay_n=self.delay_n)
        msg += f"change z motor: {steps}, {result}\n"
        # thread_log = threading.Thread(target=write_log, args=(msg,))
        # thread_log.start()
        return msg

    def start_projecting(self, image_path=None):
        self.load_variables()
        thread_log = threading.Thread(target=write_log, args=("start command",))
        thread_log.start()
        self.running = True
        # is_led_on = turn_on_off_led("on")
        update_flags(stop_printing=False, is_printing=True, num_layers=self.num_layers, is_error=False, error="")
        if image_path is not None:
            # self.reload_image(image_path)
            self.one_layer_display = True
        self.start()

    def stop_projecting(self):
        thread_log = threading.Thread(target=write_log, args=("stop command",))
        thread_log.start()
        self.running = False
        self.layer_count = 1
        update_flags(stop_printing=True, is_printing=False, is_error=False, error="",  layer_count=0, is_complete=False)
        # self.cleanup()
        # turn_on_off_led("off")
        # print("Projector stopped")
        # sys.exit()

    def pause(self):
        """Pausa el proceso."""
        self.paused = True

    def resume(self):
        """Reanuda el proceso."""
        self.paused = False

    def reload_image(self, image_path=None):
        thread_log = threading.Thread(
            target=write_log, args=(f"reload image: {image_path}",)
        )
        thread_log.start()
        if image_path:
            self.image_path = image_path

        self.texture = self.load_texture()

    def layer_count_fun(self):
        return self.layer_count

    def set_delays(self, new_delay_z, new_delay_n):
        self.delay_z_retract = new_delay_z
        self.delay_n = new_delay_n
