import conf
from crudmysql import MySQL
from conf import variables
from caja import Password
from env import variables
from mongodb import MyMongo

def cargar_datos():
    obj_MySQL = MySQL()
    obj_Pymongo = MyMongo(conf.variables)

    sql_estudiantes = "select * from estudiante"
    sql_kardex = "select * from kardex"
    sql_usuario = "select * from usuarios"

    obj_MySQL.conectar_mysql()
    lista_estudiantes = obj_MySQL.consulta_sql(sql_estudiantes)
    lista_kardex = obj_MySQL.consulta_sql(sql_kardex)
    lista_usuarios = obj_MySQL.consulta_sql(sql_usuario)
    obj_MySQL.desconectar_mysql()
    obj_Pymongo.conectar_mongodb()
    for est in lista_estudiantes:
        e = {}
        e["control"] = est[0]
        e["nombre"] = est[1]
        obj_Pymongo.insertar_mongodb("estudiante", e)

    for mat in lista_kardex:
        n = {}
        n["idKardex"] = mat[0]
        n["control"] = mat[1]
        n["materia"] = mat[2]
        n["calificacion"] = float(mat[3])
        obj_Pymongo.insertar_mongodb("kardex", n)

    for us in lista_usuarios:
        u = {}
        u["idUsuario"] = us[0]
        u["control"] = us[1]
        u["clave"] = us[2]
        u["clave_cifrada"] = us[3]
        obj_Pymongo.insertar_mongodb("usuarios", u)
    obj_Pymongo.desconectar_mongodb()

def Menu():


    while(True):
        print("-----------Menú Principal------------")
        print("1.- Insertar estudiante")
        print("2.- Actualizar calificación")
        print("3.- Consultar materias por estudiante")
        print("4.- Consulta general")
        print("5.- Eliminar estudiante")
        print("6.- Salir")
        try:
            op = int(input("Selecciona una opción: "))
        except Exception as error:
            print("ERROR", error)
            break
        else:
            if op==1:
                Insertar_estudiantesmongo()
            elif op ==2:
                Actualizar_calificacionmongo()
            elif op==3:
                Consultar_materiasmongo()
            elif op==4:
                Consulta_generalmongo()
            elif op==5:
                Eliminar_estudiantemongo()
            elif op==6:
                break
            else:
                print("Opción incorrecta")


def Insertar_estudiantesmongo():
    obj_Pymongo = MyMongo(conf.variables)
    obj_Pymongo.conectar_mongodb()
    print("INSERTAR ESTUDIANTES")
    ctrl = input("Ingresa el número de control: ")
    nombre = input("Ingresa el nombre: ")
    clave = input("Ingresa la clave de acceso: ")
    e = {
        "control": ctrl,
        "nombre": nombre
    }
    obj_usuario = Password(longitud=len(clave), contraseña=clave)
    u = {
        #SI REQUIERE EL IDUSUARIO, PERO X, SOMOS SHAVES
        "control": ctrl,
        "clave": clave,
        "clave_cifrada": obj_usuario.contraseñaCifrada
    }
    obj_Pymongo.insertar_mongodb("estudiante", e)
    obj_Pymongo.insertar_mongodb("usuarios", u)
    print("Datos insertados correctamente")
    obj_Pymongo.desconectar_mongodb()

def  Actualizar_calificacionmongo():
    obj_Pymongo = MyMongo(conf.variables)
    obj_Pymongo.conectar_mongodb()
    print("ACTUALIZAR CALIFICACIÓN")
    ctrl = input("Ingresa el número de control: ")
    materia = input("Ingresa la materia a actualizar: ")

    filtro_buscar_materia = {"control": ctrl, "materia": materia}
   # sql_buscar = f"SELECT 1 FROM kardex WHERE control = '{ctrl}' AND materia = '{materia.strip()}';"
    respuesta = obj_Pymongo.consulta_mongodb("kardex", filtro_buscar_materia)
    if respuesta:
        calificacion = int(input("Ingresa la calificacion a actualizar: "))
        json_actualiza_promedio = {
            "$set":{ "calificacion": calificacion
        }}
        resp = obj_Pymongo.actualizar_mongodb("kardex", filtro_buscar_materia, json_actualiza_promedio)
        if resp["status"]:
            print("Información actualizada")
        else:
            print("Ocurrió un error al actualizar")

    else:
        print("No encontrado")
    obj_Pymongo.desconectar_mongodb()

def  Consultar_materiasmongo():
    obj_Pymongo = MyMongo(conf.variables)

    print("MATERIAS POR ESTUDIANTE")
    #ctrl = input("Ingresa el número de control: ")
    filtro = {"control": ctrl}


    atributos_estudiante = {"_id":0, "nombre":1}
    atributos_kardex = {"_id":0, "materia":1, "calificacion":1}
    obj_Pymongo.conectar_mongodb()
    respuesta = obj_Pymongo.consulta_mongodb("estudiante", filtro, atributos_estudiante)
    respuesta2 = obj_Pymongo.consulta_mongodb("kardex", filtro, atributos_kardex)
    obj_Pymongo.desconectar_mongodb()
    if respuesta["status"] and respuesta2["status"]:
        print("Estudiante: ", respuesta["resultado"][0]["nombre"])
        for reg in respuesta2["resultado"]:
            print(reg["materia"], reg["calificacion"])



def Consulta_generalmongo():
    obj_Pymongo = MyMongo(conf.variables)
    obj_Pymongo.conectar_mongodb()
    print("CONSULTA GENERAL")
    respuesta = obj_Pymongo.consultageneral_mongodb("estudiante")
    respuesta2 = obj_Pymongo.consultageneral_mongodb("kardex")
    obj_Pymongo.desconectar_mongodb()
    i = 0;
    if respuesta["status"] and respuesta2["status"]:
        for res1 in respuesta["resultado"]:
            j=0
            prom = 0
            cont = 0
            for res2 in respuesta2["resultado"]:
                if respuesta["resultado"][i]["control"] == respuesta2["resultado"][j]["control"]:
                    prom += respuesta2["resultado"][j]["calificacion"]
                    cont += 1
                j+=1
            if(cont>0):
                prom = prom/cont
            print("CONTROL: ", respuesta["resultado"][i]["control"], " NOMBRE: ", respuesta["resultado"][i]["nombre"], " PROMEDIO: ", prom)
            i +=1



def Eliminar_estudiantemongo():
    obj_Pymongo = MyMongo(conf.variables)
    obj_Pymongo.conectar_mongodb()
    print("ELIMINAR ALUMNO")
    ctrl = input("Ingresa el número de control: ")

    filtro = {"control": ctrl}

    respuesta_estudiante = obj_Pymongo.consulta_mongodb("estudiante", filtro)
    if respuesta_estudiante["status"]:
        obj_Pymongo.eliminar_mongodb("estudiante", filtro)
        obj_Pymongo.eliminar_mongodb("kardex", filtro)
        obj_Pymongo.eliminar_mongodb("usuarios", filtro)
        print("Registro Eliminado")
    else:
        print("No encontrado")
    obj_Pymongo.desconectar_mongodb()

    #print(respuesta)
    #print(respuesta2)

#cargar_datos()
Menu()
