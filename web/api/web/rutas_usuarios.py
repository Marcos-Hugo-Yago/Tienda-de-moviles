from flask import request, Blueprint, make_response
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers, validar_session_normal
import controlador_usuarios
import json

bp = Blueprint('usuarios', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = request.json
        if login_json and "username" in login_json and "password" in login_json:
            username = login_json['username']
            password = login_json['password']
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.login_usuario(username, password)
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
    if respuesta.get("status") == "OK" and "csrf_token" in respuesta:
        response.set_cookie('csrf_token', respuesta['csrf_token'], httponly=False, samesite='Lax')
    response.headers.extend(extra_headers)
    return response

@bp.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        registro_json = request.json
        if registro_json and "username" in registro_json and "password" in registro_json:
            username = registro_json['username']
            password = registro_json['password']
            correo = registro_json.get('correo', '')
            if isinstance(username, str) and isinstance(password, str) and isinstance(correo, str) and len(username) < 50 and len(password) < 50 and len(correo) < 100:
                respuesta, code = controlador_usuarios.alta_usuario(username, password, correo)
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

@bp.route("/logout", methods=['GET'])
def logout():
    respuesta, code = controlador_usuarios.logout()
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.set_cookie('csrf_token', '', expires=0, httponly=False, samesite='Lax')
    response.headers.extend(extra_headers)
    return response
