# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:07 $"

from files.constants import settings_path


def update_settings(**kwargs):
    import json

    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    for key, value in kwargs.items():
        settings[key] = value
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)


def read_settings():
    import json

    settings = json.load(open(settings_path, "r"))
    return settings
