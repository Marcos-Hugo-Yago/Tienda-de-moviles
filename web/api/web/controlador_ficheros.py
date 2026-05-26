from __future__ import print_function
import os
import uuid
from werkzeug.utils import secure_filename
from html import escape


ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp',
    'doc', 'docx', 'xls', 'xlsx', 'csv', 'md', 'log',
    'cfg', 'xml', 'json', 'yaml', 'yml'
}

ALLOWED_MIMETYPES = {
    'text/plain', 'application/pdf', 'image/jpeg', 'image/png',
    'image/gif', 'image/bmp', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv', 'text/markdown', 'text/x-log',
    'application/xml', 'application/json',
    'application/x-yaml', 'text/yaml',
    'application/octet-stream'
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def guardar_fichero(nombre, contenido):
    try:
        nombre_seguro = secure_filename(nombre)
        if not nombre_seguro:
            return {"status": "Nombre de archivo inválido"}, 400

        ext = nombre_seguro.rsplit('.', 1)[-1].lower() if '.' in nombre_seguro else ''
        if ext not in ALLOWED_EXTENSIONS:
            return {"status": "Tipo de archivo no permitido"}, 400

        if contenido.mimetype and contenido.mimetype not in ALLOWED_MIMETYPES:
            return {"status": "Tipo MIME no permitido"}, 400

        contenido.seek(0, os.SEEK_END)
        file_size = contenido.tell()
        contenido.seek(0)
        if file_size > MAX_FILE_SIZE:
            return {"status": "El archivo excede el tamaño máximo de 5 MB"}, 400

        basepath = os.path.dirname(__file__)
        upload_dir = os.path.join(basepath, 'static/archivos')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        unique_name = f"{uuid.uuid4().hex}_{nombre_seguro}"
        ruta_fichero = os.path.join(upload_dir, unique_name)
        contenido.save(ruta_fichero)

        return {"status": "OK", "filename": unique_name}, 200
    except Exception as e:
        print(f"Excepcion al guardar el fichero: {e}", flush=True)
        return {"status": "ERROR"}, 500


def ver_fichero(nombre):
    try:
        nombre_seguro = secure_filename(nombre)
        if not nombre_seguro:
            return {"contenido": "Nombre de archivo inválido"}, 400

        basepath = os.path.dirname(__file__)
        upload_dir = os.path.join(basepath, 'static/archivos')
        ruta_fichero = os.path.join(upload_dir, nombre_seguro)

        with open(ruta_fichero, 'rb') as f:
            raw = f.read()

        try:
            contenido = raw.decode('utf-8')
        except UnicodeDecodeError:
            contenido = f"[Archivo binario - {len(raw)} bytes]"

        contenido = escape(contenido)

        return {"contenido": contenido}, 200
    except FileNotFoundError:
        return {"contenido": "Archivo no encontrado"}, 404
    except Exception as e:
        print(f"Excepcion al ver el fichero: {e}", flush=True)
        return {"contenido": ""}, 500


