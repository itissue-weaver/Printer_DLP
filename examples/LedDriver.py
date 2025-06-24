import argparse

import serial
import time

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
                time.sleep(0.5)  # Allow some time for a response
                response = self.serial_connection.read_all().decode()
                return response
            except serial.SerialException as e:
                print(f"Error sending command: {e}")
        else:
            print("Serial connection is not open.")
            return None

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Projector control")
    parser.add_argument("--state", type=str, choices=["on", "off"], default="off",
                        help="state of the led")
    parser.add_argument("--send", type=str, default="",
                        help="send a command to the projector")
    args = parser.parse_args()
    led_controller = LEDController(port="/dev/ttyUSB0", baudrate=115200)
    led_controller.connect()

    if args.send and args.send != "":
        print(f">>>{args.send+"\r\n"}<<<")
        res = led_controller.send_command(args.send)
        print(f"<<<{res}>>>")
    else:
        if args.state == "on":
            if led_controller.turn_on_led():
                print("LED turned on.")
            else:
                print("Failed to turn on LED.")
        if args.state == "off":
            if led_controller.turn_off_led():
                print("LED turned off.")
            else:
                print("Failed to turn off LED.")
    led_controller.disconnect()
