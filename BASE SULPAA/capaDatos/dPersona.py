from supabase import create_client

url = 'https://aflmusqffqglrkkmdrav.supabase.co'
key = 'sb_secret_JaaM6I6JpMgYFeFTe-21_g_fsUCjLQB'

supabase = create_client(url, key)


class DPersona:

    def mostrarPersonas(self):
        response = (
            supabase
            .table("usuario")
            .select("usuario_id, nombre, apellido, correo, telefono")
            .order("usuario_id")
            .execute()
        )
        return response.data

    def nuevaPersona(self, usuario: dict):
        supabase.table("usuario").insert({
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "correo": usuario["correo"],
            "contrasena": usuario["contrasena"],
            "telefono": usuario["telefono"]
        }).execute()

    def actualizarPersona(self, usuario: dict, correo_original: str):
        supabase.table("usuario").update({
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "correo": usuario["correo"],
            "telefono": usuario["telefono"]
        }).eq("correo", correo_original).execute()

    def eliminarPersona(self, correo: str):
        supabase.table("usuario") \
            .delete() \
            .eq("correo", correo) \
            .execute()
