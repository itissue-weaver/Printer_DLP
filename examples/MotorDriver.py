import argparse
from time import sleep
import RPi.GPIO as GPIO


from files.constants import delay_z, delay_n

import threading

from templates.AuxiliarFunctions import write_log

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
    "SWITCH_1": 27,
}


class MotorController:
    def __init__(self, pins=None, mode_spr="Full"):
        self.thread_test = None
        if pins is None:
            pins = default_pins
        self.pins = pins
        self.mode_spr = mode_spr
        self.spr = {"Full": 200}
        self.delay = 0.01
        self.delay_z = 0.005

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
        GPIO.setup(self.pins["SWITCH_3"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(self.pins["SLEEP"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_PLATE"], GPIO.HIGH)
        GPIO.output(self.pins["DIR_Z"], GPIO.HIGH)

        for pin in self.pins["EN"]:
            GPIO.output(pin, GPIO.LOW)

    def set_delays(self, delayz=delay_z, delayn=delay_n):
        self.delay = delayn
        self.delay_z = delayz
        thread_log = threading.Thread(
            target=write_log, args=(f"Delay set to {delayn} and {delayz}",)
        )
        thread_log.start()

    def rotate_motor(self, pin_dir, step_pin, direction_rotation, steps):
        try:
            GPIO.output(pin_dir, direction_rotation)
            for _ in range(steps):
                GPIO.output(step_pin, GPIO.HIGH)
                sleep(self.delay)
                GPIO.output(step_pin, GPIO.LOW)
                sleep(self.delay)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sleep(1)
            GPIO.cleanup()

    def move_z_until_switch(self, direction_rotation, switch_pin):
        try:
            GPIO.output(self.pins["DIR_Z"], direction_rotation)
            while GPIO.input(switch_pin) == GPIO.HIGH:
                GPIO.output(self.pins["STEP_Z"], GPIO.HIGH)
                sleep(self.delay_z)
                GPIO.output(self.pins["STEP_Z"], GPIO.LOW)
                sleep(self.delay_z)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sleep(1)
            GPIO.cleanup()

    def move_z(self, direction_rotation, steps):
        try:
            GPIO.output(self.pins["DIR_Z"], direction_rotation)
            for _ in range(steps):
                GPIO.output(self.pins["STEP_Z"], GPIO.HIGH)
                sleep(self.delay_z)
                GPIO.output(self.pins["STEP_Z"], GPIO.LOW)
                sleep(self.delay_z)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sleep(1)
            GPIO.cleanup()

    def move_plate_until_switch(self, direction_rotation, switch_pin):
        try:
            GPIO.output(self.pins["DIR_PLATE"], direction_rotation)
            while GPIO.input(switch_pin) == GPIO.HIGH:
                GPIO.output(self.pins["STEP_PLATE"], GPIO.HIGH)
                sleep(self.delay)
                GPIO.output(self.pins["STEP_PLATE"], GPIO.LOW)
                sleep(self.delay)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sleep(1)
            GPIO.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motors controller")
    parser.add_argument(
        "--action",
        type=str,
        choices=[
            "move_z_sw",
            "move_z",
            "move_plate_sw",
            "move_plate",
            "rotate_motor",
            "empty",
        ],
        default="empty",
        help="action to execute by the controller",
    )
    parser.add_argument(
        "--direction",
        type=str,
        choices=["ccw", "cw"],
        default="cw",
        help="direction to move the motor",
    )
    parser.add_argument(
        "--steps", type=int, default=0, help="number of steps to move the motor"
    )
    parser.add_argument(
        "--location_z",
        type=str,
        choices=["top", "bottom"],
        default="top",
        help="location to move z in case of move_z_sw",
    )
    parser.add_argument(
        "--motor",
        type=str,
        choices=["plate", "z"],
        default="z",
        help="motor to move in case of rotate_motor",
    )
    parser.add_argument(
        "--delay_z",
        type=float,
        default=delay_z,
        help="delay to move z in case of move_z_sw",
    )
    parser.add_argument(
        "--delay_n",
        type=float,
        default=delay_n,
        help="delay to move n in case of move_plate",
    )
    args = parser.parse_args()
    thread_log = threading.Thread(
        target=write_log, args=(f"Motor: {args} {args.action} {args.direction} {args.steps}",)
    )
    thread_log.start()
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
        "SWITCH_1": 27,
    }
    controller = MotorController(PINS)
    # controller.test_init_movement()
    controller.set_delays(args.delay_z, args.delay_n)
    match args.action:
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
            controller.rotate_motor(
                controller.pins["DIR_PLATE"],
                controller.pins["STEP_PLATE"],
                direction,
                args.steps,
            )
        case "move_z_sw":
            if args.direction == "cw":
                direction = GPIO.HIGH
            else:
                direction = GPIO.LOW
            if args.location_z == "bottom":
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
            print(
                "Empty action with default values: ",
                args.action,
                args.direction,
                args.steps,
                args.location_z,
                args.motor,
            )
