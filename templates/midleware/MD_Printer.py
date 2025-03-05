# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:24 $"

import json
import os
import shutil
import zipfile

import requests

from files.constants import (
    server_domain,
    base_url,
    headers,
    path_temp_zip,
    zip_file_name,
)
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


def send_zip_file(filepath=None, chunk_size=1024 * 1024):
    filepath = "files/img/temp.zip" if filepath is None else filepath
    file_size = os.path.getsize(filepath)
    with open(filepath, "rb") as f:
        for chunk_start in range(0, file_size, chunk_size):
            chunk = f.read(chunk_size)
            response = requests.post(
                f"{server_domain + base_url}/layer/zip",
                files={"file": chunk},
                headers={
                    "Content-Range": f"bytes {chunk_start}-{chunk_start + len(chunk) - 1}/{file_size}"
                },
            )
            if response.status_code != 200:
                print(f"Error en la subida: {response.text}")
                return response.status_code, f"Error en la subida: {response.text}"
    return 200, response.json()


def uncompres_files_zip():
    if os.path.exists(f"{path_temp_zip}/extracted"):
        shutil.rmtree(f"{path_temp_zip}/extracted")
        os.makedirs(f"{path_temp_zip}/extracted")
    else:
        os.makedirs(f"{path_temp_zip}/extracted")
    try:
        # Extrae todos los archivos del archivo ZIP
        with zipfile.ZipFile(f"{path_temp_zip}/{zip_file_name}", "r") as zipf:
            zipf.extractall(f"{path_temp_zip}/extracted")
        return 200, "Ok"
    except Exception as e:
        print("Error al descomprimir el archivo:", e)
        return 500, f"Error al descomprimir el archivo: {str(e)}"


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
