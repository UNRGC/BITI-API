# 🎙️ BITI-API

**API para procesamiento automático de bitácoras de soporte técnico mediante audio**

BITI-API es una aplicación de código abierto que permite convertir grabaciones de audio en bitácoras estructuradas de soporte técnico utilizando inteligencia artificial. El sistema transcribe el audio, extrae información relevante y la almacena en una base de datos para su consulta y análisis.

## 📋 ¿Qué es BITI-API?

BITI-API (Bitácoras de TI) es una API REST construida con FastAPI que automatiza el proceso de documentación de casos de soporte técnico. En lugar de escribir manualmente cada incidencia, los técnicos pueden grabar un audio describiendo el problema y la solución, y la API se encarga de:

- **Transcribir** el audio a texto usando Faster Whisper
- **Estructurar** la información mediante IA (Google Gemini)
- **Almacenar** los datos en una base de datos SQL Server
- **Consultar** y filtrar bitácoras existentes
- **Generar estadísticas** sobre casos atendidos

## ✨ Características principales

- 🎯 **Procesamiento de audio**: Sube archivos de audio y obtén bitácoras estructuradas automáticamente
- 🤖 **IA integrada**: Utiliza Google Gemini para extraer y organizar información relevante
- 📊 **Gestión de bitácoras**: CRUD completo y filtros avanzados
- 📈 **Estadísticas**: Métricas agregadas sobre casos atendidos
- 🐳 **Dockerizado**: Fácil despliegue con Docker y Docker Compose
- 📚 **Documentación automática**: Interfaz Swagger/OpenAPI incluida
- 🔌 **API REST**: Integración sencilla con cualquier sistema

## 🛠️ Tecnologías utilizadas

- **FastAPI** - Framework web moderno y de alto rendimiento
- **SQLAlchemy** - ORM para manejo de base de datos
- **Faster Whisper** - Transcripción de audio (modelo de IA optimizado)
- **Google Gemini** - Procesamiento de lenguaje natural
- **SQL Server** - Base de datos relacional
- **Docker** - Contenedorización
- **Python 3.12** - Lenguaje de programación

## 📦 Estructura del proyecto

```
BITI-API/
├── config/              # Configuración de base de datos
├── models/              # Modelos SQLAlchemy
├── repositories/        # Capa de acceso a datos
├── routers/             # Endpoints de la API
├── schemas/             # Esquemas Pydantic (validación)
├── services/            # Lógica de negocio
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias Python
├── Dockerfile           # Configuración del contenedor
├── docker-compose.yml   # Orquestación de servicios
└── .env                 # Variables de entorno (crear este archivo)
```

## 🚀 Primeros pasos

### Requisitos previos

- **Docker** y **Docker Compose** instalados
- **SQL Server** (puede ser local, remoto o en Azure)
- **API Key de Google Gemini** ([obtener aquí](https://ai.google.dev/))

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/BITI-API.git
cd BITI-API
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de la base de datos
DB_TYPE=sqlserver

# Configuración SQL Server Express
SQL_SERVER_HOST=host.docker.internal\instancia
SQL_SERVER_DATABASE=biti_db
SQL_SERVER_DRIVER='ODBC Driver 17 for SQL Server'
SQL_TRUSTED_CONNECTION=no

# Si usas autenticación SQL Server (dejar vacío para Windows Authentication)
SQL_SERVER_USER=
SQL_SERVER_PASSWORD=

# Clave API de Gemini
GEMINI_API_KEY=

# Configuración de la aplicación
ENVIRONMENT=development
DEBUG=True
```

**Nota:** Si usas SQL Server local en Windows, puedes conectarte desde Docker usando `host.docker.internal` como servidor:

```env
DB_SERVER=host.docker.internal
```

### 3. Construir y ejecutar con Docker Compose

```bash
docker-compose up --build
```

Este comando:
- Construye la imagen Docker con todas las dependencias
- Inicia el contenedor en el puerto 8000
- Configura la red y las variables de entorno

### 4. Verificar que funciona

Una vez iniciado, accede a:

- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## 📖 Uso de la API

### Procesar un archivo de audio

```bash
curl -X POST "http://localhost:8000/audio/procesar" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@tu_audio.mp3"
```

**Respuesta:**
```json
{
  "bitacora_id": 1,
  "transcripcion": "Texto transcrito del audio...",
  "datos_estructurados": {
    "cliente": "Nombre del cliente",
    "empresa": "Empresa Inc.",
    "numero_ticket": "TKT-12345",
    "tipo_solicitud": "Soporte",
    "descripcion": "Descripción del problema",
    "solucion": "Solución aplicada",
    "poliza": true
  }
}
```

### Listar bitácoras con filtros

```bash
curl -X GET "http://localhost:8000/bitacoras?cliente=Juan&fecha_inicio=2026-01-01"
```

### Obtener estadísticas

```bash
curl -X GET "http://localhost:8000/bitacoras/estadisticas?ultimos_dias=7"
```

### Ver todos los endpoints

Accede a http://localhost:8000/docs para una documentación interactiva completa con ejemplos y posibilidad de probar cada endpoint.

## 🔧 Comandos útiles de Docker

### Iniciar servicios
```bash
docker-compose up
```

### Iniciar en segundo plano
```bash
docker-compose up -d
```

### Ver logs
```bash
docker-compose logs -f
```

### Detener servicios
```bash
docker-compose down
```

### Reconstruir imagen
```bash
docker-compose up --build
```

### Acceder al contenedor
```bash
docker exec -it biti-api bash
```

## 🗄️ Configuración de la base de datos

El proyecto utiliza SQL Server. Asegúrate de:

1. Tener una instancia de SQL Server accesible
2. Crear una base de datos para el proyecto
3. Configurar las credenciales en el archivo `.env`

La aplicación creará automáticamente las tablas necesarias al iniciar.

### Modelo de datos principal

```sql
Bitacora:
- id (int, PK)
- cliente (varchar)
- empresa (varchar)
- descripcion (text)
- solucion (text)
- poliza (boolean)
- fecha (datetime)
```

## 🧪 Desarrollo sin Docker

Si prefieres ejecutar la aplicación localmente sin Docker:

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Este es un proyecto de código abierto y puedes:

1. 🍴 Hacer un fork del proyecto
2. 🔨 Crear una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. 💾 Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. 📤 Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. 🎉 Abrir un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. Siéntete libre de usarlo, modificarlo y distribuirlo.

## 🐛 Reporte de errores

Si encuentras algún error o tienes una sugerencia, por favor abre un issue en GitHub.

## ⚠️ Notas importantes

- **Seguridad**: Nunca subas tu archivo `.env` al repositorio. Ya está incluido en `.gitignore`
- **API Keys**: Mantén tus claves de API seguras y no las compartas públicamente
- **Recursos**: El procesamiento de audio puede ser intensivo en recursos. Ajusta los recursos de Docker según sea necesario
- **Modelos de IA**: La primera vez que se ejecuta puede tardar en descargar los modelos de Faster Whisper
