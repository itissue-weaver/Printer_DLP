# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:20 $"

from flask_restx import fields
from werkzeug.datastructures import FileStorage

from templates.static.constants import api

expected_files_almacen = api.parser()
expected_files_almacen.add_argument(
    "file", type=FileStorage, location="files", required=True
)

post_settings_model = api.model(
    "PostSettings",
    {"HOST": fields.String(description="Host of the server", example="127.0.0.1")},
)

# motor_config = {
#     "action": "empty",
#     "direction": "cw",
#     "steps": 0,
#     "location_z": "top",
#     "motor": "z"
# }
post_driver_motor_model = api.model(
    "PostDriveMotor",
    {
        "action": fields.String(
            description="Action to perform",
            example="move_plate",
            enum=[
                "move_z_sw",
                "move_z",
                "move_plate_sw",
                "move_plate",
                "rotate_motor",
                "empty",
            ],
        ),
        "direction": fields.String(
            description="Direction to move",
            example="cw",
            enum=["cw", "ccw"],
        ),
        "steps": fields.Integer(
            description="Number of steps to move",
            example=200,
        ),
        "location_z": fields.String(
            description="Location of the Z axis",
            example="top",
            enum=["top", "bottom"],
        ),
        "motor": fields.String(
            description="Motor to move",
            example="plate",
            enum=["plate", "z"],
        ),
        "delay_z": fields.Float(
            description="Delay of the Z axis",
            example=0.005,
        ),
        "delay_n": fields.Float(
            description="Delay of the plate",
            example=0.01,
        ),
    },
)

post_driver_led_model = api.model(
    "PostDriverLed",
    {
        "state": fields.String(
            description="State of the LED",
            example="on",
            enum=["on", "off"],
        ),
    },
)


post_driver_led_command_model = api.model(
    "PostDriverLed",
    {
        "state": fields.String(
            description="State of the LED",
            example="on",
            enum=["on", "off"],
        ),
        "command": fields.String(
            description="Command to perform",
            example="WT+LEDE=1",
        ),
    },
)