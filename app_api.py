# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:36 $"

from flask import Flask
from flask_cors import CORS

from templates.static.constants import api
from templates.resources.Projector import ns as ns_printer

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

api.init_app(app)
api.add_namespace(ns_printer)

if __name__ == "__main__":
    app.run()
