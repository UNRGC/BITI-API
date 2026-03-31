from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audio_router, bitacora_router
from config.database import init_db
import os


def _parse_csv_env(var_name: str, default: list[str]) -> list[str]:
    """Convierte variables CSV en listas limpias para configuración CORS."""
    raw_value = os.getenv(var_name)
    if raw_value is None:
        return default

    parsed_values = [item.strip() for item in raw_value.split(",") if item.strip()]
    return parsed_values or default


app = FastAPI(
    title="BITI API",
    description="API para procesamiento de bitácoras de soporte técnico mediante audio",
    version="2.0.0"
)

# CORS en producción: requiere orígenes explícitos (sin wildcard) por seguridad.
environment = os.getenv("ENVIRONMENT", "development").lower()
if environment == "production":
    cors_allow_origins = _parse_csv_env("CORS_ALLOW_ORIGINS", [])
    cors_allow_methods = _parse_csv_env(
        "CORS_ALLOW_METHODS",
        ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    cors_allow_headers = _parse_csv_env(
        "CORS_ALLOW_HEADERS",
        ["Authorization", "Content-Type", "Accept", "Origin"]
    )
    cors_allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allow_origins,
        allow_credentials=cors_allow_credentials,
        allow_methods=cors_allow_methods,
        allow_headers=cors_allow_headers,
    )

init_db()

app.include_router(audio_router.router)
app.include_router(bitacora_router.router)


@app.get("/", tags=["Raíz"])
def root():
    """Retorna metadata de la API"""
    return {
        "message": "BITI API - sistema de Bitácoras",
        "version": "2.0.0"
    }
