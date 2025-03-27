# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:07 $"

import json
from datetime import datetime

from files.constants import settings_path, materials_path, projects_path, format_timestamp


def update_settings(**kwargs):
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    for key, value in kwargs.items():
        settings[key] = value
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)


def read_settings():
    settings = json.load(open(settings_path, "r"))
    return settings


def read_materials():
    materials = json.load(open(materials_path, "r"))
    return materials


def update_materials(materials):
    with open(materials_path, "w") as f:
        json.dump(materials, f, indent=4)


def read_projects():
    projects = json.load(open(projects_path, "r"))
    return projects


def create_new_project(data):
    projects = read_projects()
    key = data.get("name").replace(" ", "").lower()
    timestamp = datetime.now().strftime(format_timestamp)
    data["timestamp"] = timestamp
    data["settings"] = {"status_frames": [0, 0, 0, 0]}
    projects[key] = data
    with open(projects_path, "w") as f:
        json.dump(projects, f, indent=4)
