# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:24 $"

import json

import requests

from files.constants import server_domain, base_url, headers
from templates.AuxiliarFunctions import read_settings


def send_start_print():
    response = requests.post(
        f"{server_domain + base_url}/start", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def send_settings_printer():
    settings = read_settings()
    response = requests.post(
        f"{server_domain + base_url}/settings",
        json=settings,
        data=json.dumps(settings),
        headers=headers,
        verify=False,
    )
    # print(f"{server_domain + base_url}/settings")
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, f"Error settings sender: {response}"


def get_settings_printer():
    response = requests.get(
        url=f"{server_domain + base_url}/settings", headers=headers, verify=False
    )
    try:
        if response.status_code == 200:
            data = response.json()
            return 200, data
        else:
            return response.status_code, None
    except Exception as e:
        return response.status_code, str(e)


def send_stop_print():
    response = requests.post(
        f"{server_domain + base_url}/stop", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def send_next_layer_file(image_path):
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        response = requests.post(f"{server_domain + base_url}/layer/file", files=files)
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def send_next_layer():
    response = requests.post(
        f"{server_domain + base_url}/next/layer", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def send_zip_file():
    with open("files/img/temp.zip", "rb") as image_file:
        files = {"file": image_file}
        response = requests.post(f"{server_domain + base_url}/layer/zip", files=files)
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def ask_status():
    response = requests.get(
        f"{server_domain + base_url}/status", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None


def test_connection():
    response = requests.get(
        f"{server_domain + base_url}/hello", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return 200, data
    else:
        return response.status_code, None
