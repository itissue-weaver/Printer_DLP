# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:21 $"

from flask_restx import Api

from templates.daemons.DLPViewer import DlpViewer

api = Api()
projector = DlpViewer()

