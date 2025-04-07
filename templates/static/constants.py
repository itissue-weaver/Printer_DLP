# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:21 $"

from flask_restx import Api

from templates.daemons.DLPViewer import DlpViewer
# from templates.daemons.MotorController import MotorController

api = Api()
projector = DlpViewer()
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

# controller_motor = MotorController(PINS)

