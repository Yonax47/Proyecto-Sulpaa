from capaLogicaNegocios.nPersona import NPersona
import streamlit as st
import re
import hashlib


class PPersona:
    def __init__(self):
        self.negocio = NPersona()

        if "editar" not in st.session_state:
            st.session_state.editar = False
        if "correo_original" not in st.session_state:
            st.session_state.correo_original = None
        if "datos_form" not in st.session_state:
            st.session_state.datos_form = {
                "nombre": "",
                "apellido": "",
                "telefono": "",
                "correo": "",
            }

        self.interfaz()

    # ================= INTERFAZ =================
    def interfaz(self):
        st.title("👥 Clientes SULPAA")

        self.formulario()
        st.divider()
        self.tabla()

    # ================= FORMULARIO =================
    def formulario(self):
        with st.form("form_usuario"):
            nombre = st.text_input(
                "Nombre",
                value=st.session_state.datos_form["nombre"]
            )
            apellido = st.text_input(
                "Apellido",
                value=st.session_state.datos_form["apellido"]
            )
            telefono = st.text_input(
                "Teléfono",
                value=st.session_state.datos_form["telefono"]
            )
            correo = st.text_input(
                "Correo",
                value=st.session_state.datos_form["correo"]
            )

            contrasena = st.text_input(
                "Contraseña",
                type="password",
                help="Solo llena este campo si deseas cambiar la contraseña"
            )

            boton = st.form_submit_button(
                "Actualizar" if st.session_state.editar else "Registrar"
            )

            if boton:
                if not self.validar_datos(
                    nombre, apellido, telefono, correo,
                    contrasena if not st.session_state.editar else "123456"
                ):
                    return

                usuario = {
                    "nombre": nombre.strip(),
                    "apellido": apellido.strip(),
                    "telefono": telefono.strip(),
                    "correo": correo.strip(),
                }

                # Solo cifrar contraseña si se escribe una nueva
                if contrasena:
                    usuario["contrasena"] = self.cifrar(contrasena)

                if st.session_state.editar:
                    self.negocio.actualizarPersona(
                        usuario,
                        st.session_state.correo_original
                    )
                    st.success("✅ Usuario actualizado")
                else:
                    usuario["contrasena"] = self.cifrar(contrasena)
                    self.negocio.nuevaPersona(usuario)
                    st.success("✅ Usuario registrado")

                self.resetear()
                st.rerun()

    # ================= TABLAA=================
    def tabla(self):
        personas = self.negocio.mostrarPersonas()

        if not personas:
            st.info("No hay usuarios registrados")
            return

        st.subheader("📋 Lista de clientes")
        st.dataframe(
            personas,
            use_container_width=True
        )

        correos = [p["correo"] for p in personas]
        seleccionado = st.selectbox("Selecciona un usuario", correos)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Editar"):
                usuario = next(p for p in personas if p["correo"] == seleccionado)

                st.session_state.datos_form = {
                    "nombre": usuario["nombre"],
                    "apellido": usuario["apellido"],
                    "telefono": usuario["telefono"],
                    "correo": usuario["correo"],
                }
                st.session_state.correo_original = usuario["correo"]
                st.session_state.editar = True
                st.rerun()

        with col2:
            if st.button("🗑 Eliminar"):
                self.negocio.eliminarPersona(seleccionado)
                st.success("🗑 Usuario eliminado")
                self.resetear()
                st.rerun()

    # ================= VALIDACIONES =================
    # la validacion recorre el campo que estas ingresando
    def validar_datos(self, nombre, apellido, telefono, correo, contrasena):
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
            st.error("❌ El nombre solo debe contener letras")
            return False

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", apellido):
            st.error("❌ El apellido solo debe contener letras")
            return False

        if not re.fullmatch(r"\d{9}", telefono):
            st.error("❌ El teléfono debe tener exactamente 9 dígitos")
            return False

        if not re.fullmatch(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            correo
        ):
            st.error("❌ Correo inválido (ejemplo: usuario@dominio.com)")
            return False

        if len(contrasena) < 6:
            st.error("❌ La contraseña debe tener al menos 6 caracteres")
            return False

        return True

    # ================= UTILIDADES =================
    def cifrar(self, texto):
        return hashlib.sha256(texto.encode()).hexdigest()

    def resetear(self):
        st.session_state.editar = False
        st.session_state.correo_original = None
        st.session_state.datos_form = {
            "nombre": "",
            "apellido": "",
            "telefono": "",
            "correo": "",
        }
