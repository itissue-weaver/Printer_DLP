from time import sleep
import RPi.GPIO as GPIO

import threading
import serial
import time
default_pins = {
        "DIR_PLATE": 7,
        "STEP_PLATE": 8,
        "DIR_Z": 19,
        "STEP_Z": 26,
        "MODE": (5, 6),
        "EN": (12, 13),
        "SLEEP": 16,
        "SWITCH_2": 23,
        "SWITCH_3": 24,
    }


class LEDController:
    def __init__(self, port="COM4", baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to the serial port: {e}")

    def send_command(self, command):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(command.encode())
                print(f"Command sent: {command}")
                time.sleep(0.5)  # Allow some time for a response
                response = self.serial_connection.read_all().decode()
                print(f"Response received: {response}")
                return response
            except serial.SerialException as e:
                print(f"Error sending command: {e}")
        else:
            print("Serial connection is not open.")

    def turn_on_led(self):
        # Turn on the LED
        response = self.send_command("WT+LEDE=1\r\n")
        if "OK" in response:
            print("LED turned on.")
            return True
        else:
            print("Failed to turn on LED.")
            return False

    def turn_off_led(self):
        # Turn off the LED
        response = self.send_command("WT+LEDE=0\r\n")
        if "OK" in response:
            print("LED turned off.")
            return True
        else:
            print("Failed to turn off LED.")
            return False

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial port closed.")


def test_print_process(controller_motor):
    pins = controller_motor.pins
    led_controller = LEDController(port="/dev/ttyUSB0", baudrate=115200)
    led_controller.connect()

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
        led_controller.disconnect()

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

    def move_z(self, direction, steps):
        GPIO.output(self.pins["DIR_Z"], direction)
        for _ in range(steps):
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
if __name__ == "__main__":
    PINS = {
        "DIR_PLATE": 7,
        "STEP_PLATE": 8,
        "DIR_Z": 19,
        "STEP_Z": 26,
        "MODE": (5, 6),
        "EN": (12, 13),
        "SLEEP": 16,
        "SWITCH_2": 23,
        "SWITCH_3": 24,
    }
    controller = MotorController(PINS)
    controller.test_init_movement()
    print("Test finished")
