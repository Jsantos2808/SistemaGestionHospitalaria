from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
import uvicorn

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API Sistema de Gestión Hospitalaria",
    description="API RESTful para la gestión de pacientes, médicos, y citas.",
    version="1.0.0"
)

# ---- SCHEMAS BASICOS PARA LA API (Pydantic) ----

class PacienteSchema(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str
    email: str
    direccion: str
    tipo_sangre: str

class PacienteResponse(PacienteSchema):
    id_paciente: int
    class Config:
        from_attributes = True

# ---- RUTAS (ENDPOINTS) ----

@app.get("/", tags=["Estado"])
def read_root():
    return {"status": "ok", "message": "API de Gestión Hospitalaria Funcionando Correctamente"}

@app.get("/pacientes", response_model=List[PacienteResponse], tags=["Pacientes"])
def get_pacientes():
    # En un entorno real, esto consultaría la base de datos a través de models.py
    # Aquí devolvemos datos mockeados para probar la API
    return [
        {
            "id_paciente": 1,
            "nombre": "Juan",
            "apellido": "Perez",
            "fecha_nacimiento": date(1980, 5, 12),
            "telefono": "555-0101",
            "email": "juan@example.com",
            "direccion": "Calle Falsa 123",
            "tipo_sangre": "O+"
        }
    ]

@app.post("/pacientes", response_model=PacienteResponse, tags=["Pacientes"])
def create_paciente(paciente: PacienteSchema):
    # En un entorno real, insertaría en BD.
    nuevo_paciente = paciente.model_dump()
    nuevo_paciente["id_paciente"] = 2
    return nuevo_paciente

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
