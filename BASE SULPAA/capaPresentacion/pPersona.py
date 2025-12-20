from capaLogicaNegocios.nPersona import NPersona
import streamlit as st
import re
import hashlib


class PPersona:
    def __init__(self):
        self.nPersona = NPersona()

        if 'modo_edicion' not in st.session_state:
            st.session_state.modo_edicion = False
        if 'correo_original' not in st.session_state:
            st.session_state.correo_original = ''

        self.construir_interfaz()

    def construir_interfaz(self):
        st.title("Registro de Usuarios")

        # -------- FORMULARIO --------
        with st.form("form_usuario"):
            nombre = st.text_input("Nombre", key="nombre")
            apellido = st.text_input("Apellido", key="apellido")
            telefono = st.text_input("Teléfono", key="telefono")
            correo = st.text_input("Correo", key="correo")
            contrasena = st.text_input("Contraseña", type="password", key="contrasena")

            if st.session_state.modo_edicion:
                btn = st.form_submit_button("Actualizar")
            else:
                btn = st.form_submit_button("Guardar")

            if btn:
                if not self.validar_datos(nombre, apellido, telefono, correo, contrasena):
                    return

                usuario = {
                    "nombre": nombre,
                    "apellido": apellido,
                    "telefono": telefono,
                    "correo": correo,
                    "contrasena": self.cifrar(contrasena)
                }

                if st.session_state.modo_edicion:
                    self.actualizar(usuario)
                else:
                    self.guardar(usuario)

        self.mostrar_tabla()

    # -------- TABLA + BOTONES --------
    def mostrar_tabla(self):
        lista = self.nPersona.mostrarPersonas()

        if not lista:
            st.info("No hay usuarios registrados")
            return

        st.subheader("Usuarios registrados")
        st.dataframe(lista, use_container_width=True)

        opciones = [u["correo"] for u in lista]
        seleccionado = st.selectbox("Selecciona un usuario", opciones)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Editar"):
                usuario = next(u for u in lista if u["correo"] == seleccionado)

                st.session_state.nombre = usuario["nombre"]
                st.session_state.apellido = usuario["apellido"]
                st.session_state.telefono = usuario["telefono"]
                st.session_state.correo = usuario["correo"]
                st.session_state.contrasena = ""

                st.session_state.correo_original = usuario["correo"]
                st.session_state.modo_edicion = True
                st.rerun()

        with col2:
            if st.button("Eliminar"):
                self.nPersona.eliminarPersona(seleccionado)
                st.success("Usuario eliminado")
                self.resetear()
                st.rerun()

    # -------- CRUD --------
    def guardar(self, usuario):
        correos = [u["correo"] for u in self.nPersona.mostrarPersonas()]
        if usuario["correo"] in correos:
            st.warning("Ese correo ya existe")
            return

        self.nPersona.nuevaPersona(usuario)
        st.success("Usuario registrado")
        self.resetear()

    def actualizar(self, usuario):
        lista = self.nPersona.mostrarPersonas()
        for u in lista:
            if u["correo"] == usuario["correo"] and u["correo"] != st.session_state.correo_original:
                st.warning("Ese correo ya pertenece a otro usuario")
                return

        self.nPersona.actualizarPersona(usuario, st.session_state.correo_original)
        st.success("Usuario actualizado")
        self.resetear()

    # -------- UTILIDADES --------
    def resetear(self):
        st.session_state.modo_edicion = False
        st.session_state.correo_original = ""
        st.session_state.nombre = ""
        st.session_state.apellido = ""
        st.session_state.telefono = ""
        st.session_state.correo = ""
        st.session_state.contrasena = ""

    def validar_datos(self, nombre, apellido, telefono, correo, contrasena):
        if not nombre.isalpha():
            st.error("Nombre inválido")
            return False
        if not apellido.isalpha():
            st.error("Apellido inválido")
            return False
        if not telefono.isdigit():
            st.error("Teléfono inválido")
            return False
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            st.error("Correo inválido")
            return False
        if len(contrasena) < 6:
            st.error("Contraseña muy corta")
            return False
        return True

    def cifrar(self, texto):
        return hashlib.sha256(texto.encode()).hexdigest()
