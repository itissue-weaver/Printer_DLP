# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 04/mar/2025 at 21:15 $"

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
    "Full": (0, 0, 0),
    "Half": (1, 0, 0),
    "1/4": (0, 1, 0),
    "1/8": (1, 1, 0),
}
PINS = {
    "DIR_PLATE": 20,
    "STEP_PLATE": 21,
    "DIR_Z": 19,
    "STEP_Z": 26,
    "MODE": (0, 5, 6),
    "EN": (12, 13),
    "SLEEP": 16,
    "SWITCH": 14,
}

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set BCM mode
GPIO.setmode(GPIO.BCM)

# Setup individual pins
GPIO.setup(PINS.get("DIR_PLATE"), GPIO.OUT)
GPIO.setup(PINS.get("STEP_PLATE"), GPIO.OUT)
GPIO.setup(PINS.get("DIR_Z"), GPIO.OUT)
GPIO.setup(PINS.get("STEP_Z"), GPIO.OUT)
GPIO.output(PINS.get("DIR_PLATE"), CW)
GPIO.output(PINS.get("DIR_Z"), CW)

GPIO.setup(PINS.get("SWITCH"), GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup MODE pins
GPIO.setup(PINS.get("MODE"), GPIO.OUT)
for pin, value in zip(PINS.get("MODE"), RESOLUTION.get("Full")):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, value)

# Setup EN pins
GPIO.setup(PINS.get("EN"), GPIO.OUT)

for pin in PINS.get("EN"):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
GPIO.setup(PINS.get("SLEEP"), GPIO.OUT)
GPIO.output(PINS.get("SLEEP"), GPIO.HIGH)


if __name__ == "__main__":
    step_count = SPR.get("Full")
    GPIO.setup(1, GPIO.OUT)
    # Enable motor
    for pin in PINS.get("EN"):
        GPIO.output(pin, GPIO.HIGH)


    delay = 0.05
    # Step forward
    for x in range(step_count):
        if GPIO.input(PINS.get("SWITCH")) == GPIO.HIGH:
            print("Switch is on")
            GPIO.output(1, GPIO.HIGH)
        else:
            print("Switch is off")
            GPIO.output(1, GPIO.LOW)
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.HIGH)
        GPIO.output(PINS.get("STEP_Z"), GPIO.HIGH)
        sleep(delay)
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.LOW)
        GPIO.output(PINS.get("STEP_Z"), GPIO.LOW)
        sleep(delay)
        print(f"step {x}")

    sleep(1)
    # Change direction
    GPIO.output(PINS.get("DIR_PLATE"), CCW)
    GPIO.output(PINS.get("DIR_Z"), CCW)
    # Step backward
    for x in range(step_count):
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.HIGH)
        GPIO.output(PINS.get("STEP_Z"), GPIO.HIGH)
        sleep(delay)
        GPIO.output(PINS.get("STEP_PLATE"), GPIO.LOW)
        GPIO.output(PINS.get("STEP_Z"), GPIO.LOW)
        sleep(delay)

    GPIO.cleanup()