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

# Example usage
if __name__ == "__main__":
    led_controller = LEDController(port="COM4", baudrate=115200)
    led_controller.connect()
    led_controller.turn_on_led()
    time.sleep(2)  # Wait for 2 seconds
    led_controller.turn_off_led()
    led_controller.disconnect()