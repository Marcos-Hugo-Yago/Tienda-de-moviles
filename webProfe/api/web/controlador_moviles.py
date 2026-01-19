from bd import obtener_conexion
import sys


def convertir_movil_a_json(movil):
    d = {}
    d['id'] = movil[0]
    d['nombre'] = movil[1]
    d['descripcion'] = movil[2]
    d['precio'] = float(movil[3])
    d['foto'] = movil[4]
    d['ingredientes']=movil[5]
    return d

def insertar_movil(nombre, descripcion, precio,foto,ingredientes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Moviles(nombre, descripcion, precio,foto,ingredientes) VALUES (%s, %s, %s,%s,%s)",
                       (nombre, descripcion, precio,foto,ingredientes))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_Moviles():
    Movilesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM Moviles")
            Moviles = cursor.fetchall()
            if Moviles:
                for movil in Moviles:
                    Movilesjson.append(convertir_movil_a_json(movil))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las Moviles", flush=True)
        code=500
    return Movilesjson,code

def obtener_movil_por_id(id):
    moviljson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM Moviles WHERE id =" + id)
            movil = cursor.fetchone()
            if movil is not None:
                moviljson = convertir_movil_a_json(movil)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una movil", flush=True)
        code=500
    return moviljson,code
def eliminar_movil(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Moviles WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una movil", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_movil(id, nombre, descripcion, precio, foto,ingredientes):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE Moviles SET nombre = %s, descripcion = %s, precio = %s, foto=%s, ingredientes=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,ingredientes,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualziar una movil", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code
