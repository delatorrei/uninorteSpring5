import sqlite3
from typing import final
from flask.wrappers import Response
from werkzeug.security import check_password_hash

def sql(query):
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return data


def check_login(**kwargs):
    nombre = kwargs['Usuario']
    password = kwargs['contrasena']
    query = f'SELECT u.nombre,u.password,u.tipo,u.validado FROM usuario u WHERE u.email="{nombre}"'
    print(query)
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchone()
        if not data:
            return response(True,"No existe el usuario") # si no encuentra coincidencias

        if data[-1] == 0:
            return response(True,"Tu cuenta esta inactiva")


        if check_password_hash(data[1], password):
            print(data)  # print
            if data[2] == 3:
                return response(datos=(data[2], data[0]))
            elif data[2] ==2:
                query = f"SELECT u.nombre,u.password,u.tipo,(m.id) as materia FROM usuario u inner JOIN materias m on u.id=m.id_usuario AND u.email='{nombre}'"
                cur.execute(query)
                data = cur.fetchone()
                return response(datos=data[2:4])  # si coninciden la contraseña
 
        return response(True, "Error al Inciar Secion")  # no coincidio la contraseña


def addActivity(datos, idMaterias):
    print(datos)
    var_file = datos.get("position","")
    var_act = datos["Nombre_de_la_Actividad"]
    var_date = datos["fecha_de_inicio"]
    var_date_end = datos["fecha_de_Entrega"]
    var_description = datos["Descripcion"]

    dbquery = f'INSERT INTO actividades (nombre,fecha_inicio,fecha_fin, id_materia,description, path_files) VALUES ("{var_act}","{var_date}","{var_date_end}",{idMaterias}, "{var_description}", "{var_file}")'

    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(dbquery)
        con.commit()

def returnActivity(idMateria):
    dbquery = f"SELECT id, nombre, description, r_image FROM actividades WHERE id_materia={idMateria}" 
    return sql(dbquery)
           

def detalleActividad(id_actividad):
    try:
        dbquery = f"""SELECT (activities.nombre) as Titulo, activities.fecha_fin, activities.path_files, activities.description ,activities.r_image, users.nombre FROM 
    ((actividades activities INNER JOIN materias subjects ON activities.id_materia=subjects.id) INNER JOIN
    usuario users ON users.id=subjects.id_usuario ) WHERE activities.id={id_actividad}"""
        return True, sql(dbquery)[0] 
    except IndexError:
        return False, None

def registrar(*args):
    try:
        cadena = f"INSERT INTO usuario (nombre,email,password,tipo, edad,sexo) VALUES ('{args[0]}','{args[1]}','{args[2]}','{args[3]}',{args[4]},'{args[5]}') "
        print(cadena)
        with sqlite3.connect("base.sqlite3") as con:
            cur = con.cursor()
            cur.execute(cadena)
            con.commit()
        return True

    except:
        print("Ha sucedido un Error")        
        return False

def Resultado(pagina):
    
    actividades = "SELECT A.nombre, A.description, (m.nombre) as n_asignatura FROM actividades A INNER JOIN materias m on A.id_materia=m.id "
    respuesta = sql(actividades)
    tamano = 10
    total_pages = len(respuesta)//tamano   
    if len(respuesta) % tamano > 0:
        total_pages += 1
    fun_inicial = (pagina-1)*tamano
    fun_final = fun_inicial+tamano
    if fun_final > len(respuesta)-1:
        fun_final = len(respuesta)        
    return respuesta[fun_inicial:fun_final ],total_pages, pagina
    

def response(error=False, mensaje="Operación exitosa", datos=None):
    res = {
        "error": error,
        "mensaje": mensaje,
        "datos": datos,
    }
    return res
