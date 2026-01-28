# 📝 Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2.0.0] - 2026-01-28

### 🎉 Versión inicial de código abierto

Primera versión pública de BITI-API como proyecto de código abierto.

### ✨ Características

- **Procesamiento de audio**: Transcripción automática con Faster Whisper
- **IA integrada**: Extracción de información estructurada con Google Gemini
- **API REST completa**: Endpoints para CRUD de bitácoras
- **Filtros avanzados**: Búsqueda por cliente, empresa, fecha, tipo, etc.
- **Estadísticas**: Métricas agregadas de casos atendidos
- **Dockerización**: Configuración completa con Docker y Docker Compose
- **Documentación**: Swagger/OpenAPI automática en `/docs`

### 🗄️ Base de datos

- Soporte para SQL Server
- Modelos SQLAlchemy
- Migraciones automáticas al iniciar

### 📚 Documentación

- README completo en español
- Guía de contribución (CONTRIBUTING.md)
- Licencia MIT
- Archivo de ejemplo de variables de entorno (.env.example)

### 🛠️ Tecnologías

- FastAPI 0.104.0+
- Python 3.12
- SQLAlchemy 2.0+
- Faster Whisper 0.9.0+
- Google Gemini AI
- Docker

### 🔧 Arquitectura

- Patrón Repository para acceso a datos
- Separación de capas: routers, services, repositories, models
- Inyección de dependencias con FastAPI
- Validación con Pydantic schemas

---

## Tipos de cambios

- `✨ Added` - Nuevas funcionalidades
- `🔧 Changed` - Cambios en funcionalidades existentes
- `⚠️ Deprecated` - Funcionalidades que serán removidas
- `🗑️ Removed` - Funcionalidades removidas
- `🐛 Fixed` - Corrección de errores
- `🔒 Security` - Correcciones de vulnerabilidades