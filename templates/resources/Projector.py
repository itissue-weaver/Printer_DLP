# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:17 $"


from flask import request
from flask_restx import Namespace, Resource
from werkzeug.utils import secure_filename

from files.constants import image_path_projector
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
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                return {"msg": "File is not an image"}, 400
            try:
                file.save(image_path_projector)
                return {"msg": f"Ok with filaname: {expected_files_almacen}"}, 200
            except Exception as e:
                print(e)
                return {"data": str(e), "msg": "Error at file structure"}, 400
        else:
            return {"msg": "No se subio el archivo"}, 400


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
        return {"msg": "Ok, projector started", "data": projector.is_alive_projector()}, 200


@ns.route("/stop")
class Stop(Resource):
    def post(self):
        # stop the print
        projector.stop_projecting()
        return {"msg": "Ok, projector stopped", "data": projector.is_alive_projector()}, 200


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
