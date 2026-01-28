from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from schemas.bitacora_schema import BitacoraResponse, BitacoraCreate
from repositories.bitacora_repository import BitacoraRepository
from config.database import get_db

router = APIRouter(
    prefix="/bitacoras",
    tags=["Bitácoras"]
)


@router.post("/", response_model=BitacoraResponse)
def crear_bitacora(datos: BitacoraCreate, db: Session = Depends(get_db)):
    """Crea un nuevo registro"""
    repo = BitacoraRepository(db)
    return repo.create(datos.model_dump())


@router.get("/estadisticas")
def obtener_estadisticas(
    ultimos_dias: int = Query(7, description="Período en días"),
    db: Session = Depends(get_db)
):
    """Retorna métricas agregadas y registros recientes"""
    repo = BitacoraRepository(db)
    return repo.obtener_estadisticas_agregadas(ultimos_dias)


@router.get("/", response_model=List[BitacoraResponse])
def listar_bitacoras(
    cliente: Optional[str] = Query(None, description="Filtrar por cliente"),
    empresa: Optional[str] = Query(None, description="Filtrar por empresa"),
    poliza: Optional[bool] = Query(None, description="Filtrar por póliza"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_fin: Optional[date] = Query(None, description="Fecha final"),
    ordenar_por: Optional[str] = Query("fecha", description="Campo para ordenar"),
    orden: Optional[str] = Query("desc", description="Orden: asc o desc"),
    db: Session = Depends(get_db)
):
    """Retorna registros filtrados y ordenados"""
    repo = BitacoraRepository(db)
    return repo.listar_con_filtros(
        cliente=cliente,
        empresa=empresa,
        poliza=poliza,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        ordenar_por=ordenar_por,
        orden=orden
    )


@router.get("/{bitacora_id}", response_model=BitacoraResponse)
def obtener_bitacora(bitacora_id: int, db: Session = Depends(get_db)):
    """Retorna un registro por ID"""
    repo = BitacoraRepository(db)
    bitacora = repo.get_by_id(bitacora_id)
    if not bitacora:
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    return bitacora


@router.put("/{bitacora_id}", response_model=BitacoraResponse)
def actualizar_bitacora(bitacora_id: int, datos: BitacoraCreate, db: Session = Depends(get_db)):
    """Actualiza un registro por ID"""
    repo = BitacoraRepository(db)
    bitacora = repo.update(bitacora_id, datos.model_dump())
    if not bitacora:
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    return bitacora


@router.delete("/{bitacora_id}")
def eliminar_bitacora(bitacora_id: int, db: Session = Depends(get_db)):
    """Elimina un registro por ID"""
    repo = BitacoraRepository(db)
    if not repo.delete(bitacora_id):
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    return {"message": "Bitácora eliminada exitosamente"}
