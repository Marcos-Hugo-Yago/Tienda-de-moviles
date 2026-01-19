from flask import request, Blueprint, jsonify
import controlador_moviles
from funciones_auxiliares import Encoder

bp = Blueprint('Moviles', __name__)

@bp.route("/",methods=["GET"])
def Moviles():
    respuesta,code= controlador_moviles.obtener_Moviles()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def movil_por_id(id):
    respuesta,code = controlador_moviles.obtener_movil_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_movil():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        movil_json = request.json
        nombre = movil_json["nombre"]
        descripcion = movil_json["descripcion"]
        precio=movil_json["precio"]
        foto=movil_json["foto"]
        ingredientes=movil_json["ingredientes"]
        respuesta,code=controlador_moviles.insertar_movil(nombre, descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_movil(id):
    respuesta,code=controlador_moviles.eliminar_movil(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_movil():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        movil_json = request.json
        id = movil_json["id"]
        nombre = movil_json["nombre"]
        descripcion = movil_json["descripcion"]
        precio=float(movil_json["precio"])
        foto=movil_json["foto"]
        ingredientes=movil_json["ingredientes"]
        respuesta,code=controlador_moviles.actualizar_movil(id,nombre,descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

