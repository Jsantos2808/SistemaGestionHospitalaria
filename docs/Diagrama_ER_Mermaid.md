# Diagrama Entidad-Relación (ER) - Sistema de Gestión Hospitalaria

A continuación se presenta el diagrama ER utilizando la sintaxis de **Mermaid**. Puedes copiar este bloque de código y pegarlo en Notion (creando un bloque de "Mermaid") o en cualquier visor de Mermaid en línea.

```mermaid
erDiagram
    PACIENTE ||--o{ CITA : "reserva"
    PACIENTE ||--o{ HISTORIAL_MEDICO : "tiene"
    MEDICO ||--o{ CITA : "atiende"
    MEDICO ||--o{ HISTORIAL_MEDICO : "escribe"
    USUARIO ||--|{ MEDICO : "es_un"
    
    PACIENTE {
        int id_paciente PK
        string nombre
        string apellido
        date fecha_nacimiento
        string telefono
        string email
        string direccion
        string tipo_sangre
    }
    
    MEDICO {
        int id_medico PK
        int id_usuario FK
        string especialidad
        string numero_licencia
    }
    
    CITA {
        int id_cita PK
        int id_paciente FK
        int id_medico FK
        datetime fecha_hora
        string estado "Programada, Completada, Cancelada"
        string motivo
    }
    
    HISTORIAL_MEDICO {
        int id_historial PK
        int id_paciente FK
        int id_medico FK
        date fecha_visita
        string diagnostico
        string tratamiento
        string notas_adicionales
    }
    
    USUARIO {
        int id_usuario PK
        string username
        string password_hash
        string rol "Administrador, Medico, Recepcionista"
        boolean activo
    }
```
