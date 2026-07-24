# Frontend — Sistema de Gestión Hospitalaria

Interfaz web en **Angular 17** del Sistema de Gestión Hospitalaria.

Para instrucciones completas de instalación y uso, consulta el [README principal](../README.md) en la raíz del repositorio.

## Desarrollo

```powershell
npm install
npm start
```

La app queda en http://127.0.0.1:4200 y consume la API en http://127.0.0.1:8001.

## Estructura relevante

```
src/app/
├── core/       # AuthService, ApiService, guard e interceptor
├── layout/     # Shell con sidebar
└── pages/      # Login, dashboard, pacientes, citas, historial
```

## Build

```powershell
ng build
```
