from capaDatos.dPersona import Dpersona

class NPersona:
    def __init__(self):
        self.__dPersona = Dpersona()

    def mostrarPersonas(self):
        return self.__dPersona.mostrarPersonas()

    def nuevaPersona(self, usuario: dict):
        self.__dPersona.nuevaPersona(usuario)

    def actualizarPersona(self, usuario: dict, correo_original: str):
        self.__dPersona.actualizarPersona(usuario, correo_original)

    def eliminarPersona(self, correo: str):
        self.__dPersona.eliminarPersona(correo)
