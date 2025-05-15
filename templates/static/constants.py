# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:21 $"

from flask_restx import Api

from templates.daemons.DLPViewer import DlpViewer

api = Api()
projector = DlpViewer()
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
# controller_motor = MotorController(PINS)

