from flask import request, Blueprint, make_response
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers, validar_session_normal
import controlador_comentarios
import json

bp = Blueprint('comentarios', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route("/", methods=['POST'])
def insertar_comentario():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        comentario_json = request.json
        if comentario_json and "usuario" in comentario_json and "descripcion" in comentario_json:
            usuario = comentario_json['usuario']
            descripcion = comentario_json['descripcion']
            if isinstance(usuario, str) and isinstance(descripcion, str) and len(usuario) < 50 and len(descripcion) < 255:
                respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 401
        else:
            respuesta = {"status": "Bad request"}
            code = 401
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response

@bp.route("/", methods=['GET'])
def consultaComentarios():
    respuesta, code = controlador_comentarios.obtener_comentarios()
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers.extend(extra_headers)
    return response
