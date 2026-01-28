from services.transcription_service import TranscriptionService
from services.ia_service import IAService
from repositories.bitacora_repository import BitacoraRepository


class AudioProcessingService:
    """Orquesta el procesamiento de audio, transcripción y persistencia"""

    def __init__(self, bitacora_repository: BitacoraRepository):
        self.transcription_service = TranscriptionService()
        self.ia_service = IAService()
        self.bitacora_repository = bitacora_repository

    async def process_audio_file(self, contenido: bytes) -> dict:
        """Ejecuta pipeline completo: transcripción → estructuración → persistencia"""
        temp_file = None
        try:
            temp_file = self.transcription_service.save_temp_audio(contenido)
            texto_detectado = self.transcription_service.transcribe_audio(temp_file)
            datos = self.ia_service.estructurar_texto(texto_detectado)
            nuevo_registro = self.bitacora_repository.create(datos)

            return {
                "status": "Registro guardado",
                "id": nuevo_registro.id,
                "datos": datos,
                "texto_original": texto_detectado
            }

        finally:
            if temp_file:
                self.transcription_service.delete_temp_audio(temp_file)
