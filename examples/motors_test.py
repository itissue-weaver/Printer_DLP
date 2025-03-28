# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 24/feb/2025  at 21:15 $"

from time import sleep
import RPi.GPIO as GPIO

CW = 1  # Clockwise Rotation value
CCW = 0  # Counterclockwise Rotation value
SPR = {
    "Full": 200,
    "Half": 400,
    "1/4": 800,
    "1/8": 1600,
}
RESOLUTION = {
    "Full": (0, 0),
    "Half": (1, 0),
    "1/4": (0, 1),
    "1/8": (1, 1),
}
PINS = {
    "DIR_PLATE": 20,
    "STEP_PLATE": 21,
    "DIR_Z": 19,
    "STEP_Z": 26,
    "MODE": (5, 6),
    "EN": (12, 13),
    "SLEEP": 16,
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS.get("DIR_PLATE"), GPIO.OUT)
GPIO.setup(PINS.get("STEP_PLATE"), GPIO.OUT)
GPIO.setup(PINS.get("DIR_Z"), GPIO.OUT)
GPIO.setup(PINS.get("STEP_Z"), GPIO.OUT)
GPIO.output(PINS.get("DIR_PLATE"), CW)
GPIO.output(PINS.get("DIR_Z"), CW)
GPIO.setup(PINS.get("MODE"), GPIO.OUT)
GPIO.setup(PINS.get("EN"), GPIO.OUT)
GPIO.output(PINS.get("MODE"), RESOLUTION.get("Full"))
GPIO.output(PINS.get("EN"), GPIO.LOW)


if __name__ == "__main__":
    step_count = SPR.get("Full")
    GPIO.output(PINS.get("EN"), GPIO.HIGH)
    delay = 0.05
    for x in range(step_count):
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.HIGH)
        GPIO.output(PINS.get("STEP_Z"), GPIO.HIGH)
        sleep(delay)
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.LOW)
        GPIO.output(PINS.get("STEP_Z"), GPIO.LOW)
        sleep(delay)

    sleep(1)
    GPIO.output(PINS.get("DIR_PLATE"), CCW)
    GPIO.output(PINS.get("DIR_Z"), CCW)
    for x in range(step_count):
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.HIGH)
        GPIO.output(PINS.get("STEP_Z"), GPIO.HIGH)
        sleep(delay)
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.LOW)
        GPIO.output(PINS.get("STEP_Z"), GPIO.LOW)
        sleep(delay)
    GPIO.cleanup()
