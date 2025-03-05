# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:05 $"

import os

settings_path = "files/settings.json"
flags_path = "files/flags.json"
image_path_projector = "files/img/temp.png"
zip_file_name = "temp.zip"
path_extracted_data = "files/img/extracted_data"
path_temp_zip = "files/img"
server_domain = "http://raspberrypi.local/"
server_domain1 = "http://localhost:5000/"
server_domain2 = "http://192.168.0.4/"
base_url = "api/v1/printer"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    # "Access-Control-Request-Method": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    # "Host": "raspberrypi.local",
    # "Accept-Encoding": "gzip",
    # "Referer": "http://raspberrypi.local",
}
