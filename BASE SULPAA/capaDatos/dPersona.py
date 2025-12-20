from conexion import ConexionDB

class Dpersona:
    def __init__(self):
        self.__db = ConexionDB().conexionSupabase()
        self.__nombreTabla = 'usuario'

    def mostrarPersonas(self):
        return self.__db.table(self.__nombreTabla).select('*').execute().data

    def nuevaPersona(self, usuario: dict):
        return self.__db.table(self.__nombreTabla).insert(usuario).execute()

    def actualizarPersona(self, usuario: dict, correo_original: str):
        return (
            self.__db
            .table(self.__nombreTabla)
            .update(usuario)
            .eq('correo', correo_original)
            .execute()
        )

    def eliminarPersona(self, correo: str):
        return (
            self.__db
            .table(self.__nombreTabla)
            .delete()
            .eq('correo', correo)
            .execute()
        )



