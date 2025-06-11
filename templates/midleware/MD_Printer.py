# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:24 $"

import json
import os
import shutil
import subprocess
import threading
import zipfile

import requests

from files.constants import (
    server_domain,
    base_url,
    headers,
    path_temp_zip,
    zip_file_name,
    ruta_script_motor,
    ruta_script_led,
    delay_z,
    delay_n,
)
from templates.AuxiliarFunctions import read_settings, write_log
from time import sleep
from templates.daemons.constants import response_queue


def send_start_print():
    response = requests.post(
        f"{server_domain + base_url}/start", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        response_queue.put((200, data))
        print(200, data)
        return 200, data
    else:
        response_queue.put((response.status_code, None))
        print(response.status_code, None)
        return response.status_code, None


def send_start_print_one_image(image_path):
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        response = requests.post(f"{server_domain + base_url}/manual_start", files=files)
    if response.status_code == 200:
        data = response.json()
        response_queue.put((200, data))
        print(200, data)
        return 200, data
    else:
        response_queue.put((response.status_code, None))
        print(response.status_code, None)
        return response.status_code, None



def send_stop_print():
    response = requests.post(
        f"{server_domain + base_url}/stop", data=json.dumps({}), headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        response_queue.put((200, data))
        print(200, data)
        return 200, data
    else:
        response_queue.put((response.status_code, None))
        print(response.status_code, None)
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
        print(200, data)
        return 200, data
    else:
        print(response.status_code, None)
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


def test_motor_post():
    try:
        response = requests.post(
            f"{server_domain + base_url}/test_motor",
            data=json.dumps({}),
            headers=headers,
        )
        if response.status_code == 200:
            data = response.json()
            return 200, data
        else:
            return response.status_code, None
    except Exception as e:
        print("Error at testing motor:", e)
        return 500, str(e)


def control_motor_from_gui(action, direction, location_z, motor, steps, delayz=delay_z, delayn=delay_n):
    try:
        response = requests.post(
            f"{server_domain + base_url}/rotate/motor",
            json={
                "action": action,
                "direction": direction,
                "location_z": location_z,
                "motor": motor,
                "steps": steps,
                "delay_z": delayz,
                "delay_n": delayn
            },
            headers=headers,
        )
        if response.status_code == 200:
            data = response.json()
            print(200, data)
            return 200, data
        else:
            print(response.status_code, None)
            return response.status_code, None
    except Exception as e:
        print("Error at testing motor:", e)
        return 500, str(e)


def control_led_from_gui(state):
    try:
        response = requests.post(
            f"{server_domain + base_url}/led",
            json={
                "state": state,
            },
            headers=headers,
        )
        if response.status_code == 200:
            data = response.json()
            print(200, data)
            return 200, data
        else:
            print(response.status_code, None)
            return response.status_code, None
    except Exception as e:
        print("Error at testing led:", e)
        return 500, str(e)


def subprocess_test():
    # argumentos = ["--speed", "150", "--direction", "backward"]
    argumentos = ["--action", "move_z_sw", "--direction", "cw", "--location_z", "top"]
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    argumentos = [
        "--action",
        "move_z_sw",
        "--direction",
        "ccw",
        "--location_z",
        "button",
    ]
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    argumentos = ["--state", "on"]
    resultado = subprocess.run(
        ["python3", ruta_script_led] + argumentos, capture_output=True, text=True
    )
    sleep(5)
    argumentos = ["--state", "off"]
    resultado = subprocess.run(
        ["python3", ruta_script_led] + argumentos, capture_output=True, text=True
    )
    argumentos = ["--action", "move_z_sw", "--direction", "cw", "--location_z", "top"]
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    argumentos = [
        "--action",
        "rotate_motor",
        "--direction",
        "cw",
        "--motor",
        "plate",
        "--steps",
        "100",
    ]
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    argumentos = [
        "--action",
        "rotate_motor",
        "--direction",
        "ccw",
        "--motor",
        "z",
        "--steps",
        "100",
    ]
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    return resultado.stdout


def subprocess_control_motor(action, direction, location_z, motor, steps, new_delay_z, new_delay_n):
    argumentos = [
        "--action",
        action,
        "--direction",
        direction,
        "--location_z",
        location_z,
        "--motor",
        motor,
        "--steps",
        str(steps),
        "--delay_z",
        str(new_delay_z),
        "--delay_n",
        str(new_delay_n)
    ]
    thread_log = threading.Thread(target=write_log, args=(f"Motor sub-pro: {argumentos}",))
    thread_log.start()
    resultado = subprocess.run(
        ["python3", ruta_script_motor] + argumentos, capture_output=True, text=True
    )
    print(resultado.stdout)
    thread_log = threading.Thread(target=write_log, args=(f"Motor result: {resultado.stdout} {resultado}",))
    thread_log.start()
    return resultado.stdout



def subprocess_control_led(state):
    argumentos = ["--state", state]
    resultado = subprocess.run(
        ["python3", ruta_script_led] + argumentos, capture_output=True, text=True
    )
    print(resultado.stdout)
    return resultado.stdout
