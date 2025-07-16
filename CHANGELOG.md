# 📋 CHANGELOG

Este archivo sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y documenta todos los cambios relevantes del proyecto.

---

## \[Unreleased]

### Agregado

* Endpoint `/api/class/create` para crear cuestionarios. *(commit: Implementación de Cuestionarios, gdavidg-27)*
* Endpoint `/api/class/assess` para evaluar respuestas de cuestionarios. *(commit: update questionary, gdavidg-27)*
* Endpoint `/api/class/quiz/<id>` para obtener un cuestionario por ID.
* Endpoint `/api/documents/upload` para subir archivos PDF. *(commit: implementación de servicio incluido de documentos, cchois)*
* Endpoint `/api/documents/<id>` para consultar metadatos de documentos.
* Endpoint `/api/documents/<id>/download` y `/api/download/<file_id>` para descarga.
* Endpoint `/api/documents/search` con filtros por título, descripción, tags y usuario.

### Cambiado

* Modelos y repositorios actualizados para reflejar estructura de datos de cuestionarios. *(commit: update models and repository, gdavidg-27)*
* Separación y organización de rutas por blueprint: `class_bp` y `documents_bp`.
* Mejora en el manejo de validaciones y estructura modular del backend.

### Corregido

* Ajustes menores en la validación de respuestas en el evaluador de cuestionarios.

---

## \[1.0.0] - 2025-07-16

### Agregado

* Estructura base del proyecto Flask. *(commit: Initial commit, Juramirezlop)*
* Conexión inicial con MongoDB mediante `mongoengine`.
* Configuración de autenticación con JWT.
* Swagger básico con `flasgger` enlazado a archivos YAML.

---

## Leyenda

* **Agregado**: para nuevas funcionalidades.
* **Cambiado**: para cambios en funcionalidades existentes.
* **Corregido**: para bugs solucionados.
* **Eliminado**: para funcionalidades eliminadas.
* **Mejorado**: para mejoras internas que no cambian el comportamiento.