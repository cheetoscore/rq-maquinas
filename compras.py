#compras.py
import streamlit as st
from sqlalchemy.orm import sessionmaker
from db_config import engine
from models import Requerimiento
import pandas as pd

Session = sessionmaker(bind=engine)

def compras_form():
    st.title("Gestión de Compras")

    # Iniciar una sesión de base de datos
    session = Session()

    try:
        # Mostrar todos los requerimientos
        st.subheader("Todos los Requerimientos")
        requerimientos = session.query(Requerimiento).all()

        if requerimientos:
            # Convertir los requerimientos a un DataFrame para mostrar
            data = [
                {
                    "ID": req.id,
                    
                    "Fecha": req.fecha_rq,
                    "Equipo": req.id_equipo,
                    "Proyecto": req.proyecto,
                    "Motivo": req.motivo,
                    "Usuario": req.usuario,
                    "Estado de Compra": req.estado_compra,
                    "Estado Aprobación": req.estado_aprobacion
                }
                for req in requerimientos
            ]
            df = pd.DataFrame(data)
            st.dataframe(df)

            # Seleccionar un requerimiento para editar
            id_to_edit = st.selectbox("Seleccione el ID del requerimiento para editar", [req.id for req in requerimientos])

            # Cargar el requerimiento seleccionado
            requerimiento_to_edit = session.query(Requerimiento).get(id_to_edit)

            if requerimiento_to_edit:
                st.subheader(f"Editar Requerimiento ID: {id_to_edit}")

                # Convertir Decimal a float para evitar errores en Streamlit
                cotizacion = float(requerimiento_to_edit.cotizacion) if requerimiento_to_edit.cotizacion is not None else 0.0
                precio_unitario = float(requerimiento_to_edit.precio_unitario) if requerimiento_to_edit.precio_unitario is not None else 0.0
                cantidad = requerimiento_to_edit.cantidad  # Mostrar la cantidad actual
                subtotal = cantidad * precio_unitario
                proveedor = st.text_input("Nombre del Proveedor", value=requerimiento_to_edit.proveedor or "")
                
                # Ajuste en el selectbox para incluir la nueva opción
                estado_compra = st.selectbox(
                    "Estado de Compra", 
                    ['Para pago', 'Para aprobación', 'Para envío', 'Enviado', 'Atendido'], 
                    index=['Para pago', 'Para aprobación', 'Para envío', 'Enviado', 'Atendido'].index(requerimiento_to_edit.estado_compra or 'Para pago')
                )
                
                guia_remision = st.text_input("Código de Guía de Remisión", value=requerimiento_to_edit.guia_remision or "")
                observacion_comp = st.text_area("Observaciones de Compra", value=requerimiento_to_edit.observacion_comp or "")

                # Editar los campos
                cotizacion = st.number_input("Cotización (Precio de cotización)", value=cotizacion, step=0.01)
                precio_unitario = st.number_input("Precio Unitario de Compra", value=precio_unitario, step=0.01)
                
                # Botón para guardar los cambios
                if st.button("Guardar Cambios"):
                    requerimiento_to_edit.cotizacion = cotizacion
                    requerimiento_to_edit.precio_unitario = precio_unitario
                    requerimiento_to_edit.subtotal = cantidad * precio_unitario
                    requerimiento_to_edit.proveedor = proveedor
                    requerimiento_to_edit.estado_compra = estado_compra
                    requerimiento_to_edit.guia_remision = guia_remision
                    requerimiento_to_edit.observacion_comp = observacion_comp
                    
                    try:
                        session.commit()
                        st.success(f"Requerimiento ID {id_to_edit} actualizado con éxito.")
                        # Refrescar la vista
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error al guardar los cambios: {e}")

        else:
            st.info("No hay requerimientos registrados.")

    finally:
        # Cerrar la sesión después de las operaciones
        session.close()

# Asegúrate de ejecutar esta función para q
