import streamlit as st
from sqlalchemy.orm import sessionmaker
from db_config import engine
from models import Requerimiento, Equipo, Proyecto
import pandas as pd
from datetime import date

Session = sessionmaker(bind=engine)

def clear_insumo_fields():
    """Función para limpiar los campos de insumos."""
    st.session_state.new_insumo = ""
    st.session_state.new_oem = ""
    st.session_state.new_cantidad = 1
    st.session_state.new_unidad = ""

def requerimientos_form():
    st.title("Gestión de Requerimientos")

    # Iniciar una sesión de base de datos
    session = Session()

    try:
        usuario_actual = st.session_state.get('usuario')

        # Inicializar campos de insumos si no existen en session_state
        if 'insumos' not in st.session_state:
            st.session_state['insumos'] = []
        if 'new_insumo' not in st.session_state:
            st.session_state['new_insumo'] = ""
        if 'new_oem' not in st.session_state:
            st.session_state['new_oem'] = ""
        if 'new_cantidad' not in st.session_state:
            st.session_state['new_cantidad'] = 1
        if 'new_unidad' not in st.session_state:
            st.session_state['new_unidad'] = ""

        # Mostrar los requerimientos creados por el usuario actual
        st.subheader("Tus Requerimientos")
        requerimientos = session.query(Requerimiento).filter_by(usuario=usuario_actual).all()

        if requerimientos:
            data = [
                {
                    "ID": req.id,
                    "Fecha": req.fecha_rq,
                    "Equipo": req.id_equipo,
                    "Proyecto": req.proyecto,
                    "Motivo": req.motivo,
                    "Estado": req.estado_equipo,
                    "Estado de Compra": req.estado_compra,
                    "Estado Aprobación": req.estado_aprobacion
                }
                for req in requerimientos
            ]
            df = pd.DataFrame(data)
            st.dataframe(df)

            id_to_delete = st.selectbox("Seleccione el ID del requerimiento para borrar", [req.id for req in requerimientos])

            if st.button("Borrar Requerimiento"):
                requerimiento_to_delete = session.query(Requerimiento).get(id_to_delete)
                session.delete(requerimiento_to_delete)
                session.commit()
                st.success(f"Requerimiento ID {id_to_delete} borrado con éxito.")
                st.session_state['active_menu'] = "Requerimientos"
                st.rerun()

        else:
            st.info("No tienes requerimientos registrados.")

        equipos = session.query(Equipo).all()
        proyectos = session.query(Proyecto).all()

        equipo_seleccionado = st.selectbox("Seleccione Equipo", [e.id_equipo for e in equipos])
        # Mostrar el nombre del equipo correspondiente al seleccionar un id_equipo
        nombre_equipo = next((e.nombre for e in equipos if e.id_equipo == equipo_seleccionado), "")
        st.write(f"Nombre del Equipo: {nombre_equipo}")
        
        proyecto_seleccionado = st.selectbox("Seleccione Proyecto", [p.nombre for p in proyectos])
        # Mostrar la fecha actual como no editable
        fecha_requerimiento = date.today()
        st.write(f"Fecha de Requerimiento: {fecha_requerimiento}")

        km_hr = st.number_input("Horas o KM del equipo", min_value=0, step=1)
        motivo = st.text_area("Descripción de la Falla")
        estado_equipo = st.selectbox("Estado del Equipo", ['Operativo', 'Inoperativo', 'Proceso'])
        acciones = st.text_area("Acciones a Tomar por la Falla")
        observacion_rq = st.text_area("Observaciones del Requerimiento")

        st.subheader("Insumos Agregados")
        for index, insumo_data in enumerate(st.session_state['insumos']):
            st.write(f"Insumo {index+1}: Material: {insumo_data['insumo']}, Código OEM: {insumo_data['oem']}, Cantidad: {insumo_data['cantidad']}, Unidad: {insumo_data['unidad']}")

        st.subheader("Agregar Insumo")
        insumo = st.text_input("Material", key="new_insumo")
        oem = st.text_input("Código de Material (OEM)", key="new_oem")
        cantidad = st.number_input("Cantidad", min_value=1, step=1, key="new_cantidad")
        unidad = st.text_input("Unidad", key="new_unidad")

        if st.button("Agregar Insumo"):
            if not insumo or not oem or not unidad:
                st.error("Todos los campos del insumo deben estar completos antes de agregar otro.")
            else:
                st.session_state['insumos'].append({
                    'insumo': insumo,
                    'oem': oem,
                    'cantidad': cantidad,
                    'unidad': unidad
                })
                clear_insumo_fields()

        if st.button("Enviar Requerimiento"):
            if not st.session_state['insumos']:
                st.error("Debe agregar al menos un insumo antes de enviar el requerimiento.")
            else:
                for insumo_data in st.session_state['insumos']:
                    nuevo_requerimiento = Requerimiento(
                        fecha_rq=fecha_requerimiento,
                        id_equipo=equipo_seleccionado,
                        proyecto=proyecto_seleccionado,
                        nombre_equipo=nombre_equipo,
                        km_hr=km_hr,
                        motivo=motivo,
                        estado_equipo=estado_equipo,
                        usuario=usuario_actual,
                        acciones=acciones,
                        insumo=insumo_data['insumo'],
                        oem=insumo_data['oem'],
                        cantidad=insumo_data['cantidad'],
                        unidad=insumo_data['unidad'],
                        observacion_rq=observacion_rq
                    )
                    session.add(nuevo_requerimiento)
                session.commit()
                st.success("Requerimientos enviados con éxito.")
                st.session_state['insumos'] = []
                st.session_state['active_menu'] = "Requerimientos"
                st.rerun()

    finally:
        session.close()

# No ejecutar la función automáticamente
