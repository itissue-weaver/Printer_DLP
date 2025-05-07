import argparse
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
        "SLEEP": 22,
        "SWITCH_2": 23,
        "SWITCH_3": 24,
        "SWITCH_0": 17,
        "SWITCH_1": 27
    }

def test_print_process(controller_motor):
    pins = controller_motor.pins
    try:
        # Mover Z en sentido horario hasta el interruptor 2
        controller_motor.move_z_until_switch(GPIO.HIGH, pins["SWITCH_2"])

        # # Rotar plato en sentido horario
        # controller.rotate_motor(pins["DIR_PLATE"], pins["STEP_PLATE"], GPIO.HIGH, 100)

        # Mover Z en sentido antihorario hasta el interruptor 3
        controller_motor.move_z_until_switch(GPIO.LOW, pins["SWITCH_3"])
        led_controller.turn_on_led()
        sleep(5)
        # Mover Z en sentido horario hasta el interruptor 2
        led_controller.turn_off_led()
        sleep(5)
        controller_motor.move_z_until_switch(GPIO.HIGH, pins["SWITCH_2"])
        sleep(1)
        # Rotar plato en sentido antihorario
        controller_motor.rotate_motor(pins["DIR_PLATE"], pins["STEP_PLATE"], GPIO.LOW, 100)
        controller_motor.move_z(GPIO.LOW, 100)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleaning up pins final")
        sleep(1)
        controller_motor.pin_cleanup()
        # led_controller.turn_off_led()

class MotorController:
    def __init__(self, pins=None, mode_spr="Full"):
        self.thread_test = None
        if pins is None:
            pins = default_pins
        self.pins = pins
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
        GPIO.setup(self.pins["SWITCH_2"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pins["SWITCH_3"], GPIO.IN,  pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.pins["SLEEP"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_PLATE"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_Z"], GPIO.HIGH)

        for pin in self.pins["EN"]:
            GPIO.output(pin, GPIO.LOW)

    def rotate_motor(self, direction_pin, step_pin, direction_rotation, steps):
        GPIO.output(direction_pin, direction_rotation)
        for _ in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.delay)

    def move_z_until_switch(self, direction_rotation, switch_pin):
        GPIO.output(self.pins["DIR_Z"], direction_rotation)
        while GPIO.input(switch_pin) == GPIO.HIGH:
            GPIO.output(self.pins["STEP_Z"], GPIO.HIGH)
            sleep(self.delay_z)
            GPIO.output(self.pins["STEP_Z"], GPIO.LOW)
            sleep(self.delay_z)

    def move_z(self, direction_rotation, steps):
        GPIO.output(self.pins["DIR_Z"], direction_rotation)
        for _ in range(steps):
            GPIO.output(self.pins["STEP_Z"], GPIO.HIGH)
            sleep(self.delay_z)
            GPIO.output(self.pins["STEP_Z"], GPIO.LOW)
            sleep(self.delay_z)

    def move_plate_until_switch(self, direction_rotation, switch_pin):
        GPIO.output(self.pins["DIR_PLATE"], direction_rotation)
        while GPIO.input(switch_pin) == GPIO.HIGH:
            GPIO.output(self.pins["STEP_PLATE"], GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.pins["STEP_PLATE"], GPIO.LOW)
            sleep(self.delay)

    def pin_cleanup(self):
        GPIO.cleanup()

    def test_init_movement(self):
        if self.thread_test is not None:
            self.thread_test.join()
            print("Thread joined")
        self.thread_test = threading.Thread(target=test_print_process, args=(self,))
        self.thread_test.start()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motors controller")
    parser.add_argument("--action", type=str, choices=["move_z_sw", "move_z", "move_plate_sw", "move_plate","rotate_motor", "empty"], default="empty",
                        help="action to execute by the controller")
    parser.add_argument("--direction", type=str, choices=["ccw", "cw"], default="cw",
                        help="direction to move the motor")
    parser.add_argument("--steps", type=int, default=0,
                        help="number of steps to move the motor")
    parser.add_argument("--location_z", type=str, choices=["top", "button"], default="top",
                        help="location to move z in case of move_z_sw")
    parser.add_argument("--motor", type=str, choices=["plate", "z"], default="z",
                        help="motor to move in case of rotate_motor")
    args = parser.parse_args()
    PINS = {
        "DIR_PLATE": 7,
        "STEP_PLATE": 8,
        "DIR_Z": 19,
        "STEP_Z": 26,
        "MODE": (5, 6),
        "EN": (12, 13),
        "SLEEP": 22,
        "SWITCH_2": 23,
        "SWITCH_3": 24,
        "SWITCH_0": 17,
        "SWITCH_1": 27
    }
    controller = MotorController(PINS)
    # controller.test_init_movement()

    match  args.action:
        case "move_z":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            controller.move_z(direction, args.steps)
        case "move_plate":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            controller.rotate_motor(controller.pins["DIR_PLATE"], controller.pins["STEP_PLATE"], direction, args.steps)
        case "move_z_sw":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            if args.location_z == "button":
                sw = controller.pins["SWITCH_3"]
            else:
                sw = controller.pins["SWITCH_2"]
            controller.move_z_until_switch(direction, sw)
        case "move_plate_sw":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            controller.move_plate_until_switch(direction, controller.pins["SWITCH_0"])
        case "rotate_motor":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            if args.motor == "plate":
                motor = controller.pins["STEP_PLATE"]
                direction_pin = controller.pins["DIR_PLATE"]
            else:
                motor = controller.pins["STEP_Z"]
                direction_pin = controller.pins["DIR_Z"]
            controller.rotate_motor(direction_pin, motor, direction, args.steps)
        case "empty":
            print("Empty action with default values: ",  args.action,  args.direction, args.steps, args.location_z, args.motor)