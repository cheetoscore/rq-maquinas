from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    name_usuario = Column(String(100), nullable=False)
    tipo_usuario = Column(Integer, nullable=False)
    dni = Column(String(15), unique=True, nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Equipo(Base):
    __tablename__ = 'equipos'
    id_equipo = Column(String(50), primary_key=True)
    nombre = Column(String(255), nullable=False)
    placa = Column(String(50))
    serie = Column(String(100))
    tipo = Column(String(100))
    marca = Column(String(100))
    modelo = Column(String(50))
    anio = Column(Integer)

class Proyecto(Base):
    __tablename__ = 'proyectos'
    id_proyecto = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Requerimiento(Base):
    __tablename__ = 'requerimientos'
    id = Column(Integer, primary_key=True)
    fecha_rq = Column(Date, nullable=False)
    id_equipo = Column(String(50), ForeignKey('equipos.id_equipo'), nullable=False)
    proyecto = Column(String(100), ForeignKey('proyectos.nombre'), nullable=False)
    nombre_equipo = Column(String(100))
    km_hr = Column(Integer, nullable=False)
    motivo = Column(Text, nullable=False)
    estado_equipo = Column(String(50), nullable=False)
    usuario = Column(String(50), ForeignKey('usuarios.usuario'), nullable=False)
    acciones = Column(Text)
    insumo = Column(String(100))
    oem = Column(String(50))
    cantidad = Column(Integer)
    unidad = Column(String(50))
    cotizacion = Column(Numeric)
    precio_unitario = Column(Numeric)
    subtotal = Column(Numeric)
    proveedor = Column(String(100))
    estado_aprobacion = Column(String(20))
    usuario_aprobado = Column(String(50))
    fecha_aprobacion = Column(Date)
    estado_compra = Column(String(50))
    guia_remision = Column(String(50))
    observacion_rq = Column(Text)
    observacion_apr = Column(Text)
    observacion_comp = Column(Text)
