from faster_whisper import WhisperModel
import os


class TranscriptionService:
    """Implementa transcripción de audio mediante modelo Whisper"""

    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def transcribe_audio(self, file_path: str, language: str = "es") -> str:
        """Convierte audio a texto mediante inferencia del modelo"""
        segments, _ = self.model.transcribe(file_path, language=language)
        texto_detectado = " ".join([s.text for s in segments])
        return texto_detectado

    @staticmethod
    def save_temp_audio(contenido: bytes, filename: str = "temp_audio.mp3") -> str:
        """Persiste bytes de audio en archivo temporal y retorna ruta"""
        with open(filename, "wb") as buffer:
            buffer.write(contenido)
        return filename

    @staticmethod
    def delete_temp_audio(file_path: str):
        """Elimina archivo temporal del sistema de archivos"""
        if os.path.exists(file_path):
            os.remove(file_path)
