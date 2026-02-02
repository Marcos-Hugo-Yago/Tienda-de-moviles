from __future__ import print_function
import os
import sys
from werkzeug.utils import secure_filename


def guardar_fichero(nombre,contenido):
    try:
        nombre_seguro = secure_filename(nombre)
        print(nombre_seguro, flush=True)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        print(basepath, flush=True)
        
        # Ensure directory exists
        upload_dir = os.path.join(basepath, 'static/archivos')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        ruta_fichero = os.path.join(upload_dir, nombre_seguro) 
        print('Archivo guardado en ' +  ruta_fichero, flush=True)
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except Exception as e:
        print(f"Excepcion al guardar el fichero: {e}", flush=True)  
        respuesta={"status": "ERROR"}
        code=500
    return respuesta, code

def ver_fichero(nombre):
    try:
        nombre_seguro = secure_filename(nombre)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        ruta_fichero = os.path.join (basepath,'static/archivos',nombre_seguro) 
        
        # Security: Use open() instead of subprocess to prevent RCE
        with open(ruta_fichero, 'r') as f:
            salida = f.read()
            
        respuesta={"contenido": salida}
        code=200
    except Exception as e:
        print(f"Excepcion al ver el fichero: {e}", flush=True)   
        respuesta={"contenido":""}
        code=500
    return respuesta,code


