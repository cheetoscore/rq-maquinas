import streamlit as st
from login import login
from requerimientos import requerimientos_form
from aprobacion import aprobacion_compra_form
from compras import compras_form

def main():
    # Inicializar el estado de sesión si no existe
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Verificar el estado de sesión
    if st.session_state['logged_in']:
        st.sidebar.title("Navegación")
        user_type = st.session_state['tipo_usuario']  # Obtiene el tipo de usuario de la sesión

        # Menú de navegación basado en el tipo de usuario
        if user_type == 1:
            # Usuario tipo 1: solo ve Requerimientos
            option = st.sidebar.selectbox("Selecciona una opción", ["Requerimientos", "Cerrar Sesión"])
        elif user_type == 2:
            # Usuario tipo 2: ve Requerimientos y Compras
            option = st.sidebar.selectbox("Selecciona una opción", ["Requerimientos", "Compras", "Cerrar Sesión"])
        elif user_type == 3:
            # Usuario tipo 3: ve Requerimientos y Aprobación
            option = st.sidebar.selectbox("Selecciona una opción", ["Requerimientos", "Aprobación Compra", "Cerrar Sesión"])

        # Manejando la selección del menú
        if option == "Requerimientos":
            requerimientos_form()
        elif option == "Compras" and user_type == 2:
            compras_form()
        elif option == "Aprobación Compra" and user_type == 3:
            aprobacion_compra_form()
        elif option == "Cerrar Sesión":
            # Cerrar sesión y reiniciar la aplicación
            if 'session' in st.session_state:
                try:
                    st.session_state['session'].close()  # Cierra la sesión de base de datos si existe
                except Exception as e:
                    st.error(f"Error al cerrar la sesión de base de datos: {e}")
                finally:
                    del st.session_state['session']
            st.session_state['logged_in'] = False
            st.session_state['usuario'] = None
            st.session_state['tipo_usuario'] = None
            st.rerun()  # Recargar la aplicación para volver al login
    else:
        login()

if __name__ == "__main__":
    main()
