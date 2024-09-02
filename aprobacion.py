import streamlit as st
from sqlalchemy.orm import sessionmaker
from db_config import engine
from models import Requerimiento
import pandas as pd
from datetime import date

Session = sessionmaker(bind=engine)

def aprobacion_compra_form():
    st.title("Aprobación de Requerimientos")

    # Iniciar una sesión de base de datos
    session = Session()

    try:
        # Mostrar los requerimientos que tienen 'estado_compra' como 'Para aprobación'
        st.subheader("Requerimientos para Aprobación")
        requerimientos = session.query(Requerimiento).filter_by(estado_compra='Para aprobación').all()

        if requerimientos:
            # Convertir los requerimientos a un DataFrame para mostrar
            data = [
                {
                    "ID": req.id,
                    "Fecha": req.fecha_rq,
                    "Equipo": req.id_equipo,
                    "Proyecto": req.proyecto,
                    "Motivo": req.motivo,
                    "Estado": req.estado_equipo,
                    "Usuario": req.usuario,
                    "Estado de Compra": req.estado_compra,
                    "Estado Aprobación": req.estado_aprobacion
                }
                for req in requerimientos
            ]
            df = pd.DataFrame(data)
            st.dataframe(df)

            # Seleccionar un requerimiento para editar
            id_to_edit = st.selectbox("Seleccione el ID del requerimiento para aprobar o desaprobar", [req.id for req in requerimientos])

            # Cargar el requerimiento seleccionado
            requerimiento_to_edit = session.query(Requerimiento).get(id_to_edit)

            if requerimiento_to_edit:
                st.subheader(f"Aprobar o Desaprobar Requerimiento ID: {id_to_edit}")

                # Seleccionar estado de aprobación
                estado_aprobacion = st.selectbox(
                    "Estado de Aprobación",
                    ['Aprobado', 'Desaprobado'],
                    index=['Aprobado', 'Desaprobado'].index(requerimiento_to_edit.estado_aprobacion or 'Aprobado')
                )

                observacion_apr = st.text_area("Observaciones de Aprobación", value=requerimiento_to_edit.observacion_apr or "")

                # Botón para guardar los cambios
                if st.button("Guardar Aprobación"):
                    requerimiento_to_edit.estado_aprobacion = estado_aprobacion
                    requerimiento_to_edit.usuario_aprobado = st.session_state['usuario']  # Usuario que aprueba
                    requerimiento_to_edit.fecha_aprobacion = date.today()
                    requerimiento_to_edit.observacion_apr = observacion_apr

                    # Solo actualiza estado_compra si se aprueba
                    if estado_aprobacion == 'Aprobado':
                        requerimiento_to_edit.estado_compra = 'Para pago'  # O cualquier otro estado según tu flujo

                    session.commit()
                    st.success(f"Requerimiento ID {id_to_edit} actualizado con éxito.")
                    st.rerun()

        else:
            st.info("No hay requerimientos para aprobación.")

    finally:
        # Cerrar la sesión después de las operaciones
        session.close()
