# Clasificación de Requerimientos y Riesgos Identificados

## 1. Requerimientos Clasificados

### 1.1 Requisitos Funcionales (FR)
- **FR-01 (Gestión de Usuarios):** El sistema debe permitir el registro, modificación y eliminación (CRUD) de usuarios con diferentes roles (Administrador, Médico, Recepcionista).
- **FR-02 (Gestión de Pacientes):** El sistema debe permitir registrar y consultar la información personal y de contacto de los pacientes.
- **FR-03 (Gestión de Citas):** El sistema debe permitir a las recepcionistas programar, reprogramar y cancelar citas médicas asignándolas a un médico específico.
- **FR-04 (Historial Médico):** Los médicos deben poder crear, consultar y actualizar el historial médico de los pacientes después de cada consulta.
- **FR-05 (Autenticación):** El sistema debe tener una pantalla de login que valide las credenciales contra la base de datos y otorgue un token JWT de sesión.

### 1.2 Requisitos No Funcionales (NFR)
- **NFR-01 (Seguridad - Autenticación):** El sistema debe requerir contraseñas encriptadas (ej. bcrypt) y soporte para sesiones basadas en tokens seguros.
- **NFR-02 (Seguridad - Privacidad):** Los datos médicos sensibles deben transmitirse únicamente a través de protocolos seguros (HTTPS).
- **NFR-03 (Rendimiento):** El tiempo de respuesta para listar pacientes o cargar historiales no debe superar los 2 segundos bajo carga normal.
- **NFR-04 (Disponibilidad):** La arquitectura del sistema debe apuntar a una disponibilidad del 99.5% durante horarios operativos.
- **NFR-05 (Concurrencia):** El backend debe soportar al menos 100 operaciones por segundo sin bloquear conexiones a la base de datos.
- **NFR-06 (Usabilidad):** La interfaz construida en Angular debe ser intuitiva y adaptable a dispositivos móviles (Responsive Design).
- **NFR-07 (Auditoría):** Toda creación o modificación de un `Historial Médico` debe dejar registro automático de la fecha, hora y usuario que realizó la acción.
- **NFR-08 (Escalabilidad):** El backend (Python/FastAPI) debe ser stateless, permitiendo escalabilidad horizontal mediante contenedores.
- **NFR-09 (Mantenibilidad):** El código debe seguir guías de estilo estándar (PEP 8 para Python) e incluir comentarios en métodos complejos.
- **NFR-10 (Compatibilidad):** La plataforma web frontend debe funcionar adecuadamente en versiones recientes de Chrome, Edge, Safari y Firefox.

---

## 2. Riesgos Identificados y Mitigación

| ID | Riesgo Identificado | Probabilidad | Impacto | Plan de Mitigación |
|----|---------------------|--------------|---------|--------------------|
| **R-01** | **Brecha de seguridad o acceso no autorizado a datos de pacientes.** | Media | Alto | Implementar encriptación fuerte de contraseñas, validación estricta de tokens JWT en cada endpoint y políticas de roles (RBAC). |
| **R-02** | **Incompatibilidad entre el Frontend (Angular) y el Backend (FastAPI).** | Alta | Medio | Definir claramente los contratos de API y generar documentación interactiva usando Swagger (incluido por defecto en FastAPI) antes de programar el frontend. |
| **R-03** | **Retraso en el desarrollo por curva de aprendizaje de tecnologías.** | Media | Medio | Seguir arquitecturas limpias y mantener los componentes de Angular simples al inicio. Usar tutoriales oficiales de FastAPI. |
| **R-04** | **Pérdida de datos por fallo en base de datos.** | Baja | Alto | Configurar copias de seguridad (backups) automáticas diarias del volumen de la base de datos en un entorno de producción. |
| **R-05** | **Problemas de rendimiento con el crecimiento de la tabla de Historias Clínicas.** | Baja | Medio | Diseñar la base de datos con índices adecuados desde el inicio (en columnas de búsqueda frecuente como ID Paciente o Fecha). |
