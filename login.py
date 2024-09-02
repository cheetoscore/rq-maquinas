import streamlit as st
from sqlalchemy.orm import sessionmaker
from db_config import engine
from models import Usuario

Session = sessionmaker(bind=engine)

def login():
    st.title("Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        session = Session()
        try:
            user = session.query(Usuario).filter_by(usuario=username, password=password).first()
            if user:
                st.success(f"Bienvenido, {user.name_usuario}")
                st.session_state['logged_in'] = True
                st.session_state['usuario'] = user.usuario
                st.session_state['tipo_usuario'] = user.tipo_usuario
            else:
                st.error("Usuario o contraseña incorrectos")
        finally:
            session.close()  # Cierra la sesión después de la consulta
