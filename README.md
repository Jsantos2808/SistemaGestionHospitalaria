# Sistema de Gestión Hospitalaria

Aplicación web cliente-servidor para la gestión de pacientes, citas médicas e historial clínico.

**Stack:** Angular 17 (frontend) · FastAPI + SQLite (backend)

---

## Características

- Autenticación con roles (Administrador, Médico, Recepcionista)
- Panel de inicio con métricas del hospital
- CRUD de pacientes
- Gestión de citas (programar, completar, cancelar)
- Historial médico por paciente
- Layout con sidebar y diseño responsive

---

## Requisitos

- [Python 3.11+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/) y npm
- Windows PowerShell (scripts de arranque incluidos)

---

## Cómo ejecutar

### Opción rápida (Windows)

Desde la raíz del proyecto:

```powershell
.\start-all.ps1
```

Esto abre el backend y el frontend en ventanas separadas.

También puedes levantar cada parte por separado:

```powershell
.\start-backend.ps1
.\start-frontend.ps1
```

### Manual

**Backend**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

**Frontend** (otra terminal)

```powershell
cd frontend
npm install
npm start
```

---

## URLs

| Servicio | URL |
|----------|-----|
| Frontend | http://127.0.0.1:4200 |
| API | http://127.0.0.1:8001 |
| Documentación Swagger | http://127.0.0.1:8001/docs |

---

## Credenciales de demo

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador |
| `medico` | `medico123` | Médico |
| `recepcion` | `recepcion123` | Recepcionista |

Al iniciar, el backend crea automáticamente una base SQLite (`backend/hospital.db`) con pacientes, citas e historiales de ejemplo.

---

## Estructura del proyecto

```
SistemaGestionHospitalaria/
├── backend/                 # API FastAPI
│   ├── main.py              # Endpoints y lógica
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── database.py          # Conexión SQLite
│   └── requirements.txt
├── frontend/                # App Angular
│   └── src/app/
│       ├── core/            # Auth, API, guards
│       ├── layout/          # Sidebar / shell
│       └── pages/           # Login, dashboard, pacientes, citas, historial
├── start-all.ps1
├── start-backend.ps1
└── start-frontend.ps1
```

---

## Módulos de la API

| Recurso | Endpoints |
|---------|-----------|
| Auth | `POST /auth/login` |
| Dashboard | `GET /dashboard/stats` |
| Pacientes | `GET/POST /pacientes`, `PUT/DELETE /pacientes/{id}` |
| Médicos | `GET /medicos` |
| Citas | `GET/POST /citas`, `PUT/DELETE /citas/{id}` |
| Historial | `GET/POST /historial`, `PUT/DELETE /historial/{id}` |

Las rutas protegidas requieren el header:

```http
Authorization: Bearer <token>
```

---

## Notas

- La API usa el puerto **8001** (configurado en `frontend/src/environments/environment.ts`).
- La documentación de análisis (requerimientos, ER, Notion/Miro) está en la carpeta `docs/`.
- Este proyecto corresponde a la asignatura **Análisis de Sistemas II**.
