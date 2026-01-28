from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from schemas.bitacora_schema import AudioProcessResponse
from services.audio_processing_service import AudioProcessingService
from repositories.bitacora_repository import BitacoraRepository
from config.database import get_db

router = APIRouter(
    prefix="/audio",
    tags=["Audio Processing"]
)


@router.post("/procesar", response_model=AudioProcessResponse)
async def procesar_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Procesa archivo de audio: transcripción, estructuración con IA y persistencia"""
    contenido = await file.read()

    bitacora_repo = BitacoraRepository(db)
    audio_service = AudioProcessingService(bitacora_repo)

    resultado = await audio_service.process_audio_file(contenido)

    return resultado
