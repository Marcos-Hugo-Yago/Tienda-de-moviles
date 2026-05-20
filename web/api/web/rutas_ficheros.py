from flask import request, Blueprint, make_response
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers, validar_session_normal
import controlador_ficheros
import json

bp = Blueprint('ficheros', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route('/', methods=['POST'])
def upload():
    if validar_session_normal():
        try:
            contenido = request.files['fichero']
            nombre = request.form.get("nombre")
            if nombre and isinstance(nombre, str) and len(nombre) < 100:
                respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 400
        except Exception as e:
            print(f"Error subiendo archivo: {e}", flush=True)
            respuesta = {"status": "ERROR"}
            code = 500
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route('/<archivo>', methods=['GET'])
def ver(archivo):
    if validar_session_normal():
        try:
            respuesta, code = controlador_ficheros.ver_fichero(archivo)
        except:
            respuesta = {"status": "ERROR"}
            code = 500
    else:
        respuesta = {"status": "Forbidden"}
        code = 403
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response
