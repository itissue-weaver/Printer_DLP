from templates.daemons.MotorController import MotorController

if __name__ == "__main__":
    PINS = {
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
    controller = MotorController(PINS)
    controller.test_init_movement()
