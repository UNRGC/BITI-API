from fastapi import FastAPI
from routers import audio_router, bitacora_router
from config.database import init_db

app = FastAPI(
    title="BITI API",
    description="API para procesamiento de bitácoras de soporte técnico mediante audio",
    version="2.0.0"
)

init_db()

app.include_router(audio_router.router)
app.include_router(bitacora_router.router)


@app.get("/", tags=["Raíz"])
def root():
    """Retorna metadata de la API"""
    return {
        "message": "BITI API - Sistema de Bitácoras",
        "version": "2.0.0"
    }
