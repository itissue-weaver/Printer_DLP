# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:07 $"

import json
from datetime import datetime

from files.constants import settings_path, materials_path, projects_path, format_timestamp, flags_path

import os


def update_settings(**kwargs):
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    for key, value in kwargs.items():
        settings[key] = value
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)


def read_settings():
    try:
        settings = json.load(open(settings_path, "r"))
    except  FileNotFoundError:
        settings = json.load(open("files/default_settings.json", "r"))
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


def read_flags():
    try:
        with open(flags_path, "r") as f:
            flags = json.load(f)
    except FileNotFoundError:
        with open("files/default_flags.json", "r") as f:
            flags = json.load(f)
    return flags


def update_flags(**kwargs):
    with open(flags_path, "r") as f:
        flags = json.load(f)
    for key, value in kwargs.items():
        flags[key] = value
    with open(flags_path, "w") as f:
        json.dump(flags, f, indent=4)


def create_new_project(data):
    projects = read_projects()
    key = data.get("name").replace(" ", "").lower()
    timestamp = datetime.now().strftime(format_timestamp)
    data["timestamp"] = timestamp
    data["settings"] = {"status_frames": [0, 0, 0, 0]}
    projects[key] = data
    with open(projects_path, "w") as f:
        json.dump(projects, f, indent=4)


def save_settings_to_project(project_key, settings):
    if project_key is None:
        print("No project selected")
        return
    projects = read_projects()
    project = projects.get(project_key)
    project["settings"] = settings
    timestamp = datetime.now().strftime(format_timestamp)
    project["timestamp"] = timestamp
    projects[project_key] = project
    # print("save project", project_key, settings["status_frames"])
    with open(projects_path, "w") as f:
        json.dump(projects, f, indent=4)


def delete_project(project_key):
    projects = read_projects()
    del projects[project_key]
    with open(projects_path, "w") as f:
        json.dump(projects, f, indent=4)


def write_log(log_text):
    # check if exist if not create
    if not os.path.exists("log.txt"):
        open("log.txt", "w").close()
    with open("log.txt", "a") as f:
        f.write(log_text + "\n")
