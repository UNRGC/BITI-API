# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a BITI-API! Este documento te guiará a través del proceso de contribución.

## 📋 Tabla de Contenidos

- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Proceso de desarrollo](#proceso-de-desarrollo)
- [Estándares de código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar errores](#reportar-errores)

## 🎯 ¿Cómo puedo contribuir?

Hay muchas formas de contribuir a BITI-API:

### 🐛 Reportar errores

Si encuentras un error:

1. Verifica que el error no haya sido reportado anteriormente
2. Abre un nuevo issue con una descripción detallada
3. Incluye pasos para reproducir el error
4. Menciona tu entorno (OS, versión de Python, Docker, etc.)

### 💡 Sugerir mejoras

¿Tienes una idea para mejorar el proyecto?

1. Abre un issue describiendo tu propuesta
2. Explica por qué sería útil
3. Proporciona ejemplos de uso si es posible

### 📝 Mejorar documentación

La documentación siempre puede mejorar:

- Corregir errores tipográficos
- Agregar ejemplos
- Mejorar explicaciones
- Traducir a otros idiomas

### 💻 Contribuir código

Consulta la sección [Proceso de desarrollo](#proceso-de-desarrollo) más abajo.

## 🔧 Proceso de desarrollo

### 1. Fork y clona el repositorio

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/tu-usuario/BITI-API.git
cd BITI-API
```

### 2. Crea una rama para tu trabajo

```bash
git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/correccion-de-bug
```

Usa prefijos descriptivos:
- `feature/` para nuevas funcionalidades
- `fix/` para correcciones de errores
- `docs/` para cambios en documentación
- `refactor/` para refactorización de código
- `test/` para agregar o modificar tests

### 3. Configura tu entorno de desarrollo

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Realiza tus cambios

- Escribe código claro y mantenible
- Sigue los estándares de código (ver abajo)
- Agrega comentarios cuando sea necesario
- Actualiza la documentación si es relevante

### 5. Prueba tus cambios

```bash
# Ejecuta la aplicación localmente
uvicorn main:app --reload

# O con Docker
docker-compose up --build
```

Verifica que:
- La aplicación inicia sin errores
- Tus cambios funcionan como se esperaba
- No rompiste funcionalidades existentes
- La documentación de Swagger se actualiza correctamente (http://localhost:8000/docs)

### 6. Commit y push

```bash
# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: agregar funcionalidad X"
# o
git commit -m "fix: corregir problema Y"

# Push a tu fork
git push origin feature/mi-nueva-funcionalidad
```

### 7. Crea un Pull Request

1. Ve a tu fork en GitHub
2. Haz clic en "Pull Request"
3. Describe tus cambios detalladamente
4. Referencia issues relacionados si los hay

## 📏 Estándares de código

### Estilo Python

Seguimos [PEP 8](https://peps.python.org/pep-0008/):

```python
# ✅ Bueno
def procesar_audio(archivo: UploadFile) -> dict:
    """Procesa un archivo de audio y retorna los datos estructurados."""
    resultado = transcribir(archivo)
    return resultado

# ❌ Evitar
def ProcesarAudio(archivo):
    resultado=transcribir(archivo)
    return resultado
```

### Nombres

- **Variables y funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Módulos**: `snake_case.py`

### Type hints

Usa anotaciones de tipo siempre que sea posible:

```python
def crear_bitacora(datos: dict, db: Session) -> BitacoraModel:
    # ...
```

### Docstrings

Documenta funciones públicas:

```python
def obtener_estadisticas(ultimos_dias: int) -> dict:
    """
    Obtiene estadísticas agregadas de bitácoras.
    
    Args:
        ultimos_dias: Número de días a considerar
        
    Returns:
        dict: Diccionario con métricas calculadas
    """
    # ...
```

### Estructura de archivos

Mantén la arquitectura del proyecto:

```
- config/         # Configuración
- models/         # Modelos de base de datos
- repositories/   # Capa de acceso a datos
- routers/        # Endpoints API
- schemas/        # Validación con Pydantic
- services/       # Lógica de negocio
```

### Imports

Ordena los imports:

```python
# 1. Librerías estándar
from datetime import datetime
from typing import List, Optional

# 2. Librerías de terceros
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 3. Módulos locales
from models.bitacora_model import BitacoraModel
from schemas.bitacora_schema import BitacoraResponse
```

## 🔄 Proceso de Pull Request

1. **Espera la revisión**: Un mantenedor revisará tu PR
2. **Responde a comentarios**: Si hay sugerencias, discútelas o impleméntalas
3. **Actualiza si es necesario**: Puedes hacer commits adicionales al mismo PR
4. **Aprobación**: Una vez aprobado, tu código será fusionado
5. **Celebra**: ¡Acabas de contribuir a BITI-API! 🎉

### Checklist antes de enviar PR

- [ ] Mi código sigue los estándares del proyecto
- [ ] He probado mis cambios localmente
- [ ] He actualizado la documentación relevante
- [ ] Mi commit tiene un mensaje descriptivo
- [ ] No hay errores de sintaxis o linting
- [ ] Los cambios son mínimos y enfocados (un PR = una funcionalidad)

## 🐛 Reportar errores

### Plantilla de reporte de error

```markdown
**Descripción del error**
Una descripción clara del problema.

**Pasos para reproducir**
1. Ir a '...'
2. Ejecutar '...'
3. Ver error

**Comportamiento esperado**
Lo que debería pasar.

**Comportamiento actual**
Lo que realmente pasa.

**Capturas de pantalla**
Si aplica, agrega capturas.

**Entorno:**
- OS: [e.g. Windows 11]
- Python: [e.g. 3.12]
- Docker: [e.g. 24.0.0]

**Información adicional**
Cualquier otro contexto relevante.
```

## 💬 ¿Preguntas?

Si tienes preguntas sobre cómo contribuir:

1. Revisa los issues existentes
2. Abre un nuevo issue con la etiqueta "question"
3. Sé específico sobre lo que necesitas

## 🙏 Agradecimientos

Cada contribución, sin importar cuán pequeña sea, es valorada y apreciada. ¡Gracias por ayudar a mejorar BITI-API!