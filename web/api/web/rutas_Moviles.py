from flask import request, Blueprint, make_response
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers, validar_session_normal, validar_session_admin
import controlador_moviles
import json

bp = Blueprint('Moviles', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route("/", methods=["GET"])
def Moviles():
    if validar_session_normal():
        respuesta, code = controlador_moviles.obtener_Moviles()
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route("/<id>", methods=["GET"])
def movil_por_id(id):
    if validar_session_normal():
        respuesta, code = controlador_moviles.obtener_movil_por_id(id)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route("/", methods=["POST"])
def guardar_movil():
    if validar_session_normal():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            movil_json = request.json
            if movil_json and all(k in movil_json for k in ("nombre", "descripcion", "precio", "foto", "ingredientes")):
                nombre = movil_json["nombre"]
                descripcion = movil_json["descripcion"]
                precio = movil_json["precio"]
                foto = movil_json["foto"]
                ingredientes = movil_json["ingredientes"]
                if (isinstance(nombre, str) and isinstance(descripcion, str) and isinstance(ingredientes, str) and isinstance(foto, str)
                        and len(nombre) < 100 and len(descripcion) < 255 and len(ingredientes) < 100 and len(foto) < 500):
                    try:
                        precio = float(precio)
                    except (ValueError, TypeError):
                        respuesta = {"status": "Bad parameters"}
                        code = 400
                        response = make_response(json.dumps(respuesta, cls=Encoder), code)
                        response.headers.extend(extra_headers)
                        return response
                    respuesta, code = controlador_moviles.insertar_movil(nombre, descripcion, precio, foto, ingredientes)
                else:
                    respuesta = {"status": "Bad parameters"}
                    code = 400
            else:
                respuesta = {"status": "Bad request"}
                code = 400
        else:
            respuesta = {"status": "Bad request"}
            code = 400
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_movil(id):
    if validar_session_admin():
        respuesta, code = controlador_moviles.eliminar_movil(id)
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route("/", methods=["PUT"])
def actualizar_movil():
    if validar_session_admin():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            movil_json = request.json
            if movil_json and all(k in movil_json for k in ("id", "nombre", "descripcion", "precio", "foto", "ingredientes")):
                id = movil_json["id"]
                nombre = movil_json["nombre"]
                descripcion = movil_json["descripcion"]
                precio = movil_json["precio"]
                foto = movil_json["foto"]
                ingredientes = movil_json["ingredientes"]
                if (isinstance(nombre, str) and isinstance(descripcion, str) and isinstance(ingredientes, str) and isinstance(foto, str)
                        and len(nombre) < 100 and len(descripcion) < 255 and len(ingredientes) < 100 and len(foto) < 500):
                    try:
                        precio = float(precio)
                    except (ValueError, TypeError):
                        respuesta = {"status": "Bad parameters"}
                        code = 400
                        response = make_response(json.dumps(respuesta, cls=Encoder), code)
                        response.headers.extend(extra_headers)
                        return response
                    respuesta, code = controlador_moviles.actualizar_movil(id, nombre, descripcion, precio, foto, ingredientes)
                else:
                    respuesta = {"status": "Bad parameters"}
                    code = 400
            else:
                respuesta = {"status": "Bad request"}
                code = 400
        else:
            respuesta = {"status": "Bad request"}
            code = 400
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response
