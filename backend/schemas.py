from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# ---- Auth ----
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    rol: str
    nombre: str


# ---- Pacientes ----
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str
    email: str
    direccion: str
    tipo_sangre: str


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(PacienteBase):
    pass


class PacienteResponse(PacienteBase):
    id_paciente: int

    class Config:
        from_attributes = True


# ---- Medicos ----
class MedicoResponse(BaseModel):
    id_medico: int
    especialidad: str
    numero_licencia: str
    nombre: str

    class Config:
        from_attributes = True


# ---- Citas ----
class CitaBase(BaseModel):
    id_paciente: int
    id_medico: int
    fecha_hora: datetime
    motivo: str
    estado: str = "Programada"


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_medico: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None


class CitaResponse(BaseModel):
    id_cita: int
    id_paciente: int
    id_medico: int
    fecha_hora: datetime
    estado: str
    motivo: str
    paciente_nombre: Optional[str] = None
    medico_nombre: Optional[str] = None
    especialidad: Optional[str] = None

    class Config:
        from_attributes = True


# ---- Historial ----
class HistorialBase(BaseModel):
    id_paciente: int
    id_medico: int
    fecha_visita: date
    diagnostico: str
    tratamiento: str
    notas_adicionales: str = ""


class HistorialCreate(HistorialBase):
    pass


class HistorialUpdate(BaseModel):
    fecha_visita: Optional[date] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    notas_adicionales: Optional[str] = None
    id_medico: Optional[int] = None


class HistorialResponse(BaseModel):
    id_historial: int
    id_paciente: int
    id_medico: int
    fecha_visita: date
    diagnostico: str
    tratamiento: str
    notas_adicionales: Optional[str] = None
    paciente_nombre: Optional[str] = None
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True


# ---- Dashboard ----
class DashboardStats(BaseModel):
    total_pacientes: int
    citas_hoy: int
    citas_programadas: int
    total_historiales: int
