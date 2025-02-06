# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:35 $"

from app_api import app
from templates.AuxiliarFunctions import read_settings

if __name__ == "__main__":
    settings = read_settings()
    app.run(host=settings.get("HOST", "127.0.0.1"), port=5000, debug=True)
