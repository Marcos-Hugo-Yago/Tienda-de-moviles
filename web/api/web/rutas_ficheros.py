from flask import request, Blueprint, make_response
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers, validar_session_normal
import controlador_ficheros
import json

bp = Blueprint('ficheros', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route('/', methods=['POST'])
def upload():
    if not validar_session_normal():
        respuesta = {"status": "Forbidden"}
        return make_response(json.dumps(respuesta, cls=Encoder), 403)

    if 'fichero' not in request.files:
        respuesta = {"status": "No se envió ningún archivo"}
        return make_response(json.dumps(respuesta, cls=Encoder), 400)

    contenido = request.files['fichero']
    if not contenido.filename:
        respuesta = {"status": "No se seleccionó ningún archivo"}
        return make_response(json.dumps(respuesta, cls=Encoder), 400)

    nombre = request.form.get("nombre")
    if not nombre or not isinstance(nombre, str) or len(nombre) > 100:
        respuesta = {"status": "Bad parameters"}
        return make_response(json.dumps(respuesta, cls=Encoder), 400)

    respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route('/<archivo>', methods=['GET'])
def ver(archivo):
    if not validar_session_normal():
        respuesta = {"status": "Forbidden"}
        code = 403
    else:
        respuesta, code = controlador_ficheros.ver_fichero(archivo)
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response
