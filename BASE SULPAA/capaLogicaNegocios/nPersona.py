from capaDatos.dPersona import DPersona


class NPersona:

    def __init__(self):
        self.datos = DPersona()

    def mostrarPersonas(self):
        return self.datos.mostrarPersonas()

    def nuevaPersona(self, usuario: dict):
        self.datos.nuevaPersona(usuario)

    def actualizarPersona(self, usuario: dict, correo_original: str):
        self.datos.actualizarPersona(usuario, correo_original)

    def eliminarPersona(self, correo: str):
        self.datos.eliminarPersona(correo)
