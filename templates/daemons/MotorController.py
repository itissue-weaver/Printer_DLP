from time import sleep
import RPi.GPIO as GPIO

import threading

default_pins = {
        "DIR_PLATE": 7,
        "STEP_PLATE": 8,
        "DIR_Z": 19,
        "STEP_Z": 26,
        "MODE": (5, 6),
        "EN": (12, 13),
        "SLEEP": 16,
        "SWITCH_2": 2,
        "SWITCH_3": 3,
    }

def test_print_process(controller):
    pins = controller.pins
    try:
        # Mover Z en sentido horario hasta el interruptor 2
        controller.move_z_until_switch(GPIO.HIGH, pins["SWITCH_2"])

        # Rotar plato en sentido horario
        controller.rotate_motor(pins["DIR_PLATE"], pins["STEP_PLATE"], GPIO.HIGH, 100)

        # Mover Z en sentido antihorario hasta el interruptor 3
        controller.move_z_until_switch(GPIO.LOW, pins["SWITCH_3"])

        # Rotar plato en sentido antihorario
        controller.rotate_motor(pins["DIR_PLATE"], pins["STEP_PLATE"], GPIO.LOW, 100)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleaning up pins final")
        controller.pin_cleanup()

class MotorController:
    def __init__(self, pins=None, mode_spr="Full"):
        self.thread_test = None
        if pins is None:
            pins = default_pins
        self.pins = pins
        print(self.pins)
        self.mode_spr = mode_spr
        self.spr = {"Full": 200}
        self.delay = 0.01
        self.delay_z = 0.001

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pins["DIR_PLATE"], GPIO.OUT)
        GPIO.setup(self.pins["STEP_PLATE"], GPIO.OUT)
        GPIO.setup(self.pins["DIR_Z"], GPIO.OUT)
        GPIO.setup(self.pins["STEP_Z"], GPIO.OUT)
        GPIO.setup(self.pins["MODE"], GPIO.OUT)
        GPIO.setup(self.pins["EN"], GPIO.OUT)
        GPIO.setup(self.pins["SLEEP"], GPIO.OUT)
        GPIO.setup(self.pins["SWITCH_2"], GPIO.IN)
        GPIO.setup(self.pins["SWITCH_3"], GPIO.IN)

        GPIO.output(self.pins["SLEEP"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_PLATE"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_Z"], GPIO.HIGH)

        for pin in self.pins["EN"]:
            GPIO.output(pin, GPIO.LOW)

    def rotate_motor(self, direction_pin, step_pin, direction, steps):
        GPIO.output(direction_pin, direction)
        for _ in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.delay)

    def move_z_until_switch(self, direction, switch_pin):
        GPIO.output(self.pins["DIR_Z"], direction)
        while GPIO.input(switch_pin) == GPIO.HIGH:
            GPIO.output(self.pins["STEP_Z"], GPIO.HIGH)
            sleep(self.delay_z)
            GPIO.output(self.pins["STEP_Z"], GPIO.LOW)
            sleep(self.delay_z)

    def pin_cleanup(self):
        GPIO.cleanup()

    def test_init_movement(self):
        if self.thread_test is not None:
            self.thread_test.join()
            print("Thread joined")
        self.thread_test = threading.Thread(target=test_print_process, args=(self,))
        self.thread_test.start()