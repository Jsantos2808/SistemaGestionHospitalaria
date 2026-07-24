from datetime import date, datetime, timedelta
from hashlib import sha256
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal, engine, get_db
from models import Base, Cita, HistorialMedico, Medico, Paciente, Usuario
from schemas import (
    CitaCreate,
    CitaResponse,
    CitaUpdate,
    DashboardStats,
    HistorialCreate,
    HistorialResponse,
    HistorialUpdate,
    LoginRequest,
    LoginResponse,
    MedicoResponse,
    PacienteCreate,
    PacienteResponse,
    PacienteUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Sistema de Gestión Hospitalaria",
    description="API RESTful para pacientes, médicos, citas e historial clínico.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tokens simples en memoria para la demo académica
ACTIVE_TOKENS: dict[str, dict] = {}


def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Usuario).first():
            return

        admin = Usuario(
            username="admin",
            password_hash=hash_password("admin123"),
            rol="Administrador",
            activo=True,
        )
        medico_user = Usuario(
            username="medico",
            password_hash=hash_password("medico123"),
            rol="Medico",
            activo=True,
        )
        recepcion = Usuario(
            username="recepcion",
            password_hash=hash_password("recepcion123"),
            rol="Recepcionista",
            activo=True,
        )
        cardio = Usuario(
            username="cardio",
            password_hash=hash_password("cardio123"),
            rol="Medico",
            activo=True,
        )
        pediatra = Usuario(
            username="pediatra",
            password_hash=hash_password("pediatra123"),
            rol="Medico",
            activo=True,
        )
        db.add_all([admin, medico_user, recepcion, cardio, pediatra])
        db.flush()

        medicos = [
            Medico(id_usuario=medico_user.id_usuario, especialidad="Medicina General", numero_licencia="LIC-1001"),
            Medico(id_usuario=cardio.id_usuario, especialidad="Cardiología", numero_licencia="LIC-1002"),
            Medico(id_usuario=pediatra.id_usuario, especialidad="Pediatría", numero_licencia="LIC-1003"),
        ]
        db.add_all(medicos)
        db.flush()

        pacientes = [
            Paciente(
                nombre="Juan",
                apellido="Pérez",
                fecha_nacimiento=date(1985, 3, 12),
                telefono="555-0101",
                email="juan.perez@email.com",
                direccion="Calle Principal 123",
                tipo_sangre="O+",
            ),
            Paciente(
                nombre="María",
                apellido="García",
                fecha_nacimiento=date(1992, 7, 22),
                telefono="555-0202",
                email="maria.garcia@email.com",
                direccion="Av. Central 45",
                tipo_sangre="A+",
            ),
            Paciente(
                nombre="Carlos",
                apellido="López",
                fecha_nacimiento=date(1978, 11, 5),
                telefono="555-0303",
                email="carlos.lopez@email.com",
                direccion="Boulevard Norte 89",
                tipo_sangre="B-",
            ),
        ]
        db.add_all(pacientes)
        db.flush()

        ahora = datetime.now().replace(minute=0, second=0, microsecond=0)
        citas = [
            Cita(
                id_paciente=pacientes[0].id_paciente,
                id_medico=medicos[0].id_medico,
                fecha_hora=ahora + timedelta(hours=2),
                estado="Programada",
                motivo="Consulta general",
            ),
            Cita(
                id_paciente=pacientes[1].id_paciente,
                id_medico=medicos[1].id_medico,
                fecha_hora=ahora + timedelta(days=1, hours=3),
                estado="Programada",
                motivo="Control cardiológico",
            ),
            Cita(
                id_paciente=pacientes[2].id_paciente,
                id_medico=medicos[0].id_medico,
                fecha_hora=ahora - timedelta(days=2),
                estado="Completada",
                motivo="Dolor de espalda",
            ),
        ]
        db.add_all(citas)

        historiales = [
            HistorialMedico(
                id_paciente=pacientes[2].id_paciente,
                id_medico=medicos[0].id_medico,
                fecha_visita=date.today() - timedelta(days=2),
                diagnostico="Lumbalgia mecánica",
                tratamiento="Analgésicos y fisioterapia",
                notas_adicionales="Reposo relativo 5 días",
            ),
            HistorialMedico(
                id_paciente=pacientes[0].id_paciente,
                id_medico=medicos[1].id_medico,
                fecha_visita=date.today() - timedelta(days=15),
                diagnostico="Hipertensión leve",
                tratamiento="Dieta baja en sodio, control de presión",
                notas_adicionales="Seguimiento en 30 días",
            ),
        ]
        db.add_all(historiales)
        db.commit()
    finally:
        db.close()


seed_data()


def require_auth(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autenticado")
    token = authorization.replace("Bearer ", "", 1)
    user = ACTIVE_TOKENS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return user


def medico_display_name(db: Session, medico: Medico) -> str:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == medico.id_usuario).first()
    if usuario:
        return f"Dr(a). {usuario.username.title()} ({medico.especialidad})"
    return f"Médico #{medico.id_medico}"


def cita_to_response(db: Session, cita: Cita) -> CitaResponse:
    paciente = db.query(Paciente).filter(Paciente.id_paciente == cita.id_paciente).first()
    medico = db.query(Medico).filter(Medico.id_medico == cita.id_medico).first()
    return CitaResponse(
        id_cita=cita.id_cita,
        id_paciente=cita.id_paciente,
        id_medico=cita.id_medico,
        fecha_hora=cita.fecha_hora,
        estado=cita.estado,
        motivo=cita.motivo,
        paciente_nombre=f"{paciente.nombre} {paciente.apellido}" if paciente else None,
        medico_nombre=medico_display_name(db, medico) if medico else None,
        especialidad=medico.especialidad if medico else None,
    )


def historial_to_response(db: Session, h: HistorialMedico) -> HistorialResponse:
    paciente = db.query(Paciente).filter(Paciente.id_paciente == h.id_paciente).first()
    medico = db.query(Medico).filter(Medico.id_medico == h.id_medico).first()
    return HistorialResponse(
        id_historial=h.id_historial,
        id_paciente=h.id_paciente,
        id_medico=h.id_medico,
        fecha_visita=h.fecha_visita,
        diagnostico=h.diagnostico,
        tratamiento=h.tratamiento,
        notas_adicionales=h.notas_adicionales,
        paciente_nombre=f"{paciente.nombre} {paciente.apellido}" if paciente else None,
        medico_nombre=medico_display_name(db, medico) if medico else None,
    )


# ---- Auth ----
@app.post("/auth/login", response_model=LoginResponse, tags=["Auth"])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == payload.username).first()
    if not user or user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    if not user.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    token = sha256(f"{user.username}:{datetime.utcnow().isoformat()}".encode()).hexdigest()
    ACTIVE_TOKENS[token] = {
        "id_usuario": user.id_usuario,
        "username": user.username,
        "rol": user.rol,
    }
    return LoginResponse(
        access_token=token,
        username=user.username,
        rol=user.rol,
        nombre=user.username.title(),
    )


@app.get("/", tags=["Estado"])
def read_root():
    return {"status": "ok", "message": "API de Gestión Hospitalaria Funcionando Correctamente"}


@app.get("/dashboard/stats", response_model=DashboardStats, tags=["Dashboard"])
def dashboard_stats(db: Session = Depends(get_db), _user=Depends(require_auth)):
    hoy = date.today()
    inicio = datetime.combine(hoy, datetime.min.time())
    fin = datetime.combine(hoy, datetime.max.time())
    return DashboardStats(
        total_pacientes=db.query(Paciente).count(),
        citas_hoy=db.query(Cita).filter(Cita.fecha_hora >= inicio, Cita.fecha_hora <= fin).count(),
        citas_programadas=db.query(Cita).filter(Cita.estado == "Programada").count(),
        total_historiales=db.query(HistorialMedico).count(),
    )


# ---- Pacientes ----
@app.get("/pacientes", response_model=list[PacienteResponse], tags=["Pacientes"])
def list_pacientes(db: Session = Depends(get_db), _user=Depends(require_auth)):
    return db.query(Paciente).order_by(Paciente.id_paciente).all()


@app.get("/pacientes/{id_paciente}", response_model=PacienteResponse, tags=["Pacientes"])
def get_paciente(id_paciente: int, db: Session = Depends(get_db), _user=Depends(require_auth)):
    paciente = db.query(Paciente).filter(Paciente.id_paciente == id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@app.post("/pacientes", response_model=PacienteResponse, tags=["Pacientes"])
def create_paciente(payload: PacienteCreate, db: Session = Depends(get_db), _user=Depends(require_auth)):
    paciente = Paciente(**payload.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


@app.put("/pacientes/{id_paciente}", response_model=PacienteResponse, tags=["Pacientes"])
def update_paciente(
    id_paciente: int,
    payload: PacienteUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_auth),
):
    paciente = db.query(Paciente).filter(Paciente.id_paciente == id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for key, value in payload.model_dump().items():
        setattr(paciente, key, value)
    db.commit()
    db.refresh(paciente)
    return paciente


@app.delete("/pacientes/{id_paciente}", tags=["Pacientes"])
def delete_paciente(id_paciente: int, db: Session = Depends(get_db), _user=Depends(require_auth)):
    paciente = db.query(Paciente).filter(Paciente.id_paciente == id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.query(Cita).filter(Cita.id_paciente == id_paciente).delete()
    db.query(HistorialMedico).filter(HistorialMedico.id_paciente == id_paciente).delete()
    db.delete(paciente)
    db.commit()
    return {"ok": True, "message": "Paciente eliminado"}


# ---- Medicos ----
@app.get("/medicos", response_model=list[MedicoResponse], tags=["Medicos"])
def list_medicos(db: Session = Depends(get_db), _user=Depends(require_auth)):
    medicos = db.query(Medico).all()
    return [
        MedicoResponse(
            id_medico=m.id_medico,
            especialidad=m.especialidad,
            numero_licencia=m.numero_licencia,
            nombre=medico_display_name(db, m),
        )
        for m in medicos
    ]


# ---- Citas ----
@app.get("/citas", response_model=list[CitaResponse], tags=["Citas"])
def list_citas(db: Session = Depends(get_db), _user=Depends(require_auth)):
    citas = db.query(Cita).order_by(Cita.fecha_hora.desc()).all()
    return [cita_to_response(db, c) for c in citas]


@app.post("/citas", response_model=CitaResponse, tags=["Citas"])
def create_cita(payload: CitaCreate, db: Session = Depends(get_db), _user=Depends(require_auth)):
    if not db.query(Paciente).filter(Paciente.id_paciente == payload.id_paciente).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    if not db.query(Medico).filter(Medico.id_medico == payload.id_medico).first():
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    cita = Cita(**payload.model_dump())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita_to_response(db, cita)


@app.put("/citas/{id_cita}", response_model=CitaResponse, tags=["Citas"])
def update_cita(
    id_cita: int,
    payload: CitaUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_auth),
):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(cita, key, value)
    db.commit()
    db.refresh(cita)
    return cita_to_response(db, cita)


@app.delete("/citas/{id_cita}", tags=["Citas"])
def delete_cita(id_cita: int, db: Session = Depends(get_db), _user=Depends(require_auth)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
    return {"ok": True, "message": "Cita eliminada"}


# ---- Historial ----
@app.get("/historial", response_model=list[HistorialResponse], tags=["Historial"])
def list_historial(
    id_paciente: Optional[int] = None,
    db: Session = Depends(get_db),
    _user=Depends(require_auth),
):
    q = db.query(HistorialMedico)
    if id_paciente is not None:
        q = q.filter(HistorialMedico.id_paciente == id_paciente)
    items = q.order_by(HistorialMedico.fecha_visita.desc()).all()
    return [historial_to_response(db, h) for h in items]


@app.post("/historial", response_model=HistorialResponse, tags=["Historial"])
def create_historial(payload: HistorialCreate, db: Session = Depends(get_db), _user=Depends(require_auth)):
    if not db.query(Paciente).filter(Paciente.id_paciente == payload.id_paciente).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    if not db.query(Medico).filter(Medico.id_medico == payload.id_medico).first():
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    historial = HistorialMedico(**payload.model_dump())
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial_to_response(db, historial)


@app.put("/historial/{id_historial}", response_model=HistorialResponse, tags=["Historial"])
def update_historial(
    id_historial: int,
    payload: HistorialUpdate,
    db: Session = Depends(get_db),
    _user=Depends(require_auth),
):
    historial = db.query(HistorialMedico).filter(HistorialMedico.id_historial == id_historial).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(historial, key, value)
    db.commit()
    db.refresh(historial)
    return historial_to_response(db, historial)


@app.delete("/historial/{id_historial}", tags=["Historial"])
def delete_historial(id_historial: int, db: Session = Depends(get_db), _user=Depends(require_auth)):
    historial = db.query(HistorialMedico).filter(HistorialMedico.id_historial == id_historial).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    db.delete(historial)
    db.commit()
    return {"ok": True, "message": "Historial eliminado"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
