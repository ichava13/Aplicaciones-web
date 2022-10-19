import pymongo
from conf import variables
class  MyMongo():
    def __init__(self, variables):  ##host="localhost", db="opensource", port="27017", timeout=1000, user="", password=""
        self.MONGO_DATABASE = variables["db"]
        self.MONGO_URI = 'mongodb://'+variables["host"]+":"+str(variables["port"])
        self.MONGO_CLIENT = None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT = 1000

    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=variables["timeout"])
            
        except Exception as error:
            print("Error", error)
        else:
            print("CONEXIÓN A MONGO REALIZADA")
       # finally:
        #    if MONGO_CLIENT:
         #       MONGO_CLIENT.close()
    
    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
           self.MONGO_CLIENT.close()
            
    def consulta_mongodb(self, tabla, filtro, atributos={"_id":0}):
        response = {"status": False, "resultado":[]}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find(filtro, atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True

            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)

        return response

    def consultageneral_mongodb(self, tabla):
        response = {"status": False, "resultado":[]}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find({})
        if self.MONGO_RESPUESTA:
            response["status"] = True

            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)

        return response
    def insertar_mongodb(self, tabla, documento):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(documento)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
        else:
            return None

    def actualizar_mongodb(self, tabla, filtro, nuevosvalores):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_many(filtro, nuevosvalores)
        if self.MONGO_RESPUESTA:
            response["status"] = True
        return response
    def eliminar_mongodb(self, tabla, filtro):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_many(filtro)
        if self.MONGO_RESPUESTA:
            response["status"] = True
        return response
alumno = {
    "control":200,
    "nombre":"Peter Pan"
}
def Estud():
    tupla = set()
    with open("Estudiantes.prn") as archivo:
        for line in archivo:
            tupla.add((line[0:8], line[8:-1]))
    return tupla
def cargar_datos():
    obj_mongo = MyMongo(variables)
    obj_mongo.conectar_mongodb()
    lista_estudiantes = Estud()
    for ctrl, nom in lista_estudiantes:
        diccionario = {}
        diccionario["control"] = ctrl
        diccionario["nombre"] = nom
        obj_mongo.insertarestudiante_mongodb(diccionario)
    obj_mongo.desconectar_mongodb()
    print(lista_estudiantes)


#cargar_datos()
#obj_mongo = MyMongo(variables)
#obj_mongo.conectar_mongodb()
#obj_mongo.consulta_mongodb("estudiante")
#obj_mongo.desconectar_mongodb()
#obj_mongo.conectar_mongodb()

#obj_mongo.insertarestudiante_mongodb(alumno)

