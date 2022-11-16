import json

from crudmysql import MySQL

def Promedio_estudiante():
    obj_Mysql = MySQL(bd="itj_estudiantes")
    obj_Mysql.conectar_mysql()
    print("PROMEDIO DE ESTUDIANTE")
    ctrl = input("Ingresa el número de control: ")
    sql = f"SELECT E.control, E.nombre, format(avg(K.calificacion),1) as promedio from Estudiante E, Kardex k where E.control = k.control AND E.control = '{ctrl}';"
    respuesta = obj_Mysql.consulta_sql(sql)
    dicc = {
        "estudiante": respuesta[0][1],
        "promedio": respuesta[0][2]
    }
    obj_Mysql.desconectar_mysql()
    j = json.dumps(dicc, indent=3)
    print(j)

Promedio_estudiante()