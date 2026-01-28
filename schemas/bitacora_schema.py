from pydantic import BaseModel
from datetime import datetime


class BitacoraBase(BaseModel):
    """Schema base con campos comunes de dominio"""
    cliente: str
    empresa: str
    poliza: bool
    problema: str
    solucion: str
    monto: float


class BitacoraCreate(BitacoraBase):
    """DTO para operaciones de creación/actualización"""
    pass


class BitacoraResponse(BitacoraBase):
    """DTO de respuesta con metadatos del sistema"""
    id: int
    fecha: datetime

    class Config:
        from_attributes = True


class AudioProcessResponse(BaseModel):
    """DTO de respuesta para pipeline de procesamiento de audio"""
    status: str
    id: int
    datos: dict
    texto_original: str
