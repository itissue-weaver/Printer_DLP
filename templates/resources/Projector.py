# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:17 $"

import os

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.utils import secure_filename

from files.constants import image_path_projector, path_extracted_data
from templates.AuxiliarFunctions import read_settings, update_settings
from templates.models.printer_models import expected_files_almacen, post_settings_model
from templates.static.constants import projector

ns = Namespace("api/v1/printer")


@ns.route("/layer/file")
class LayerFile(Resource):
    @ns.expect(expected_files_almacen)
    def post(self):
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            # check if file is an image
            if not filename.lower().endswith((".zip", ".jpg", ".jpeg")):
                return {"msg": "File is not an image"}, 400
            try:
                file.save(image_path_projector)
                return {"msg": f"Ok with filaname: {expected_files_almacen}"}, 200
            except Exception as e:
                print(e)
                return {"data": str(e), "msg": "Error at file structure"}, 400
        else:
            return {"msg": "No se subio el archivo"}, 400


@ns.route("/layer/zip")
class LayerZip(Resource):
    def post(self):
        # Comprobar si el encabezado Content-Range está presente
        content_range = request.headers.get("Content-Range")
        if not content_range:
            return {"msg": "Falta el encabezado Content-Range"}, 400
        # Validar y extraer información del rango
        try:
            _, range_data = content_range.split(" ")
            byte_range, total_size = range_data.split("/")
            range_start, range_end = map(int, byte_range.split("-"))
            total_size = int(total_size)
        except Exception as e:
            return {"msg": f"Error al procesar Content-Range: {str(e)}"}, 400

        # Verificar si se envió un archivo
        file = request.files.get("file")
        if not file:
            return {"msg": "No se subió el archivo"}, 400

        # Validar que sea un archivo ZIP
        filename = secure_filename(file.filename)
        if not filename.lower().endswith(".zip"):
            return {"msg": "El archivo no es un ZIP válido"}, 400

        # Guardar el fragmento en un archivo temporal
        temp_file_path = os.path.join(path_extracted_data, f"temp_{filename}")
        try:
            with open(temp_file_path, "ab") as temp_file:  # Append binary
                temp_file.write(file.read())
        except Exception as e:
            return {"msg": f"Error al guardar el fragmento: {str(e)}"}, 500

        # Verificar si el archivo completo ha sido recibido
        if range_end + 1 == total_size:  # Todos los bytes recibidos
            final_file_path = os.path.join(path_extracted_data, filename)
            os.rename(temp_file_path, final_file_path)
            return {"msg": f"Archivo subido exitosamente: {filename}"}, 200

        # Responder si el fragmento fue recibido pero falta más
        return ({"msg": "Fragmento recibido, esperando más datos"},)


@ns.route("/settings")
class Settings(Resource):
    def get(self):
        settings = read_settings()
        if not settings:
            return {"msg": "No settings found"}, 404
        return {"data": settings, "msg": "Ok"}, 200

    @ns.expect(post_settings_model)
    def post(self):
        # save the settings
        data = ns.payload
        if not data:
            return {"msg": "No data found"}, 400
        update_settings(**data)
        return {"msg": "Ok"}, 200


@ns.route("/start")
class Start(Resource):
    def post(self):
        # start the print
        projector.start_projecting()
        return {
            "msg": "Ok, projector started",
            "data": projector.is_alive_projector(),
        }, 200


@ns.route("/stop")
class Stop(Resource):
    def post(self):
        # stop the print
        projector.stop_projecting()
        return {
            "msg": "Ok, projector stopped",
            "data": projector.is_alive_projector(),
        }, 200


@ns.route("/next/layer")
class NextLayer(Resource):
    def post(self):
        # next layer
        projector.star_reload()
        return {"msg": "Ok, next layer", "data": projector.layer_count()}, 200


@ns.route("/status")
class Status(Resource):
    def get(self):
        # status
        flag = projector.is_alive_projector()
        if flag:
            return {"msg": "Ok, projector is alive", "data": flag}, 200
        else:
            return {"msg": "Ok, projector is not alive", "data": flag}, 200
