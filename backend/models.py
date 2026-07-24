from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    rol = Column(String) # Admin, Medico, Recepcionista
    activo = Column(Boolean, default=True)

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    fecha_nacimiento = Column(Date)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)
    tipo_sangre = Column(String)
    
    # Relaciones
    citas = relationship("Cita", back_populates="paciente")
    historiales = relationship("HistorialMedico", back_populates="paciente")

class Medico(Base):
    __tablename__ = "medicos"

    id_medico = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    especialidad = Column(String)
    numero_licencia = Column(String)

    # Relaciones
    citas = relationship("Cita", back_populates="medico")
    historiales = relationship("HistorialMedico", back_populates="medico")

class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"))
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"))
    fecha_hora = Column(DateTime)
    estado = Column(String) # Programada, Completada, Cancelada
    motivo = Column(String)

    # Relaciones
    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")

class HistorialMedico(Base):
    __tablename__ = "historial_medico"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente"))
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"))
    fecha_visita = Column(Date)
    diagnostico = Column(String)
    tratamiento = Column(String)
    notas_adicionales = Column(String)

    # Relaciones
    paciente = relationship("Paciente", back_populates="historiales")
    medico = relationship("Medico", back_populates="historiales")
