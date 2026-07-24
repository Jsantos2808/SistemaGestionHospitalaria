# Guía para Documentación en Notion y Mapa en Miro

Como IA, no puedo crear directamente el tablero dentro de tu cuenta de Miro ni las páginas de tu cuenta de Notion. Sin embargo, aquí tienes la estructura y los pasos exactos para que tu documentación quede perfecta y profesional.

## 1. Documentación en Notion

Crea una nueva página en Notion llamada **"Sistema de Gestión Hospitalaria"** y añade las siguientes sub-páginas (o secciones):

### Sección A: Resumen del Proyecto
- **Objetivo:** Desarrollar un sistema de gestión hospitalaria eficiente con arquitectura cliente-servidor usando Python (FastAPI) y Angular.
- **Tecnologías:** FastAPI, SQLAlchemy, Angular, TypeScript.

### Sección B: Requerimientos y Riesgos
- Copia y pega todo el contenido del archivo `Requerimientos_y_Riesgos.md` que se encuentra en esta misma carpeta `docs/`. Notion reconocerá el formato Markdown automáticamente (incluyendo tablas y listas).

### Sección C: Arquitectura y Diseño de Datos
- Crea un bloque de código en Notion tecleando `/mermaid` (elige el bloque Mermaid).
- Pega el código del archivo `Diagrama_ER_Mermaid.md` dentro del bloque. Notion renderizará el diagrama visualmente al instante.

---

## 2. Mapa en Miro (Arquitectura del Sistema)

Para el mapa en Miro, te sugiero diseñar un **Diagrama de Arquitectura de Solución** (System Architecture Map) en lugar del ER (ya que el ER ya está en Mermaid).

### Pasos en Miro:
1. Abre un tablero nuevo.
2. Agrega una gran caja a la izquierda llamada **"Cliente / Frontend"**.
   - Dentro, pon un ícono de Angular (Representa la UI Web).
   - Añade etiquetas: "Módulo Pacientes", "Módulo Citas", "Módulo Historial".
3. Agrega una caja central llamada **"Servidor / Backend"**.
   - Dentro, pon un ícono de Python/FastAPI.
   - Añade etiquetas: "Autenticación JWT", "REST API", "ORM (SQLAlchemy)".
4. Agrega una caja a la derecha llamada **"Base de Datos"**.
   - Añade un ícono de base de datos relacional (ej. PostgreSQL o SQLite).
5. **Conexiones:**
   - Dibuja flechas bidireccionales entre Angular y FastAPI con el texto: `HTTP / REST (JSON)`.
   - Dibuja flechas bidireccionales entre FastAPI y la Base de Datos con el texto: `SQL Queries`.
6. Añade notas adhesivas (stickies) alrededor destacando los NFR:
   - Sticky amarillo cerca de la BD: *"NFR-09: Backups automáticos"*
   - Sticky azul sobre las flechas HTTP: *"NFR-02: Encriptación SSL/TLS"*
   - Sticky verde sobre Angular: *"NFR-06: Diseño Responsivo"*

Con esto, tendrás un Mapa de Miro profesional que complementa perfectamente tu diagrama ER en Mermaid.
