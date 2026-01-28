from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any

from models.bitacora_model import Bitacora


class BitacoraRepository:
    """Capa de acceso a datos para entidad Bitácora"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, datos: dict) -> Bitacora:
        """Persiste nueva entidad y retorna instancia hidratada"""
        nuevo_registro = Bitacora(
            cliente=datos.get('cliente', 'Desconocido'),
            empresa=datos.get('empresa', 'Desconocido'),
            poliza=datos.get('poliza', False),
            problema=datos.get('problema', 'Sin descripción del problema'),
            solucion=datos.get('solucion', 'Pendiente de resolución'),
            monto=datos.get('monto', 0.0)
        )
        self.db.add(nuevo_registro)
        self.db.commit()
        self.db.refresh(nuevo_registro)
        return nuevo_registro

    def get_by_id(self, bitacora_id: int) -> Optional[Bitacora]:
        """Recupera entidad por clave primaria"""
        return self.db.query(Bitacora).filter(Bitacora.id == bitacora_id).first()


    def update(self, bitacora_id: int, datos: dict) -> Optional[Bitacora]:
        """Actualiza atributos de entidad existente y persiste cambios"""
        bitacora = self.get_by_id(bitacora_id)
        if bitacora:
            for key, value in datos.items():
                setattr(bitacora, key, value)
            self.db.commit()
            self.db.refresh(bitacora)
        return bitacora

    def delete(self, bitacora_id: int) -> bool:
        """Elimina entidad por clave primaria"""
        bitacora = self.get_by_id(bitacora_id)
        if bitacora:
            self.db.delete(bitacora)
            self.db.commit()
            return True
        return False

    def obtener_estadisticas_agregadas(self, ultimos_dias: int = 7) -> Dict[str, Any]:
        """Obtiene métricas agregadas y registros recientes del período especificado"""
        fecha_limite = datetime.now() - timedelta(days=ultimos_dias)

        registros_recientes = (self.db.query(Bitacora)
                               .filter(Bitacora.fecha >= fecha_limite)
                               .order_by(desc(Bitacora.fecha))
                               .all())

        hace_4_semanas = datetime.now() - timedelta(weeks=4)
        agregado_semanal = (self.db.query(
            extract('week', Bitacora.fecha).label('semana'),
            func.sum(Bitacora.monto).label('total')
        )
                            .filter(Bitacora.fecha >= hace_4_semanas)
                            .group_by(extract('week', Bitacora.fecha))
                            .order_by('semana')
                            .all())

        hace_1_anio = datetime.now() - timedelta(days=365)
        agregado_mensual = (self.db.query(
            extract('year', Bitacora.fecha).label('anio'),
            extract('month', Bitacora.fecha).label('mes'),
            func.sum(Bitacora.monto).label('total')
        )
                            .filter(Bitacora.fecha >= hace_1_anio)
                            .group_by(extract('year', Bitacora.fecha), extract('month', Bitacora.fecha))
                            .order_by('anio', 'mes')
                            .all())

        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        total_registros = len(registros_recientes)
        suma_total = sum(r.monto for r in registros_recientes)

        return {
            "periodo": f"Últimos {ultimos_dias} días",
            "total_registros": total_registros,
            "suma_total": float(suma_total),
            "registros_recientes": registros_recientes,
            "agregado_semanal": [{
                "semana": int(r.semana),
                "total": float(r.total or 0)
            } for r in agregado_semanal],
            "agregado_mensual": [{
                "anio": int(r.anio),
                "mes": int(r.mes),
                "mes_nombre": meses[int(r.mes) - 1],
                "total": float(r.total or 0)
            } for r in agregado_mensual]
        }

    def listar_con_filtros(
            self,
            cliente: Optional[str] = None,
            empresa: Optional[str] = None,
            poliza: Optional[bool] = None,
            fecha_inicio: Optional[date] = None,
            fecha_fin: Optional[date] = None,
            ordenar_por: str = "fecha",
            orden: str = "desc"
    ) -> list[type[Bitacora]]:
        """Retorna registros filtrados y ordenados según parámetros"""
        query = self.db.query(Bitacora)

        if cliente:
            query = query.filter(Bitacora.cliente.ilike(f"%{cliente}%"))

        if empresa:
            query = query.filter(Bitacora.empresa.ilike(f"%{empresa}%"))

        if poliza is not None:
            query = query.filter(Bitacora.poliza == poliza)

        if fecha_inicio:
            query = query.filter(Bitacora.fecha >= fecha_inicio)

        if fecha_fin:
            query = query.filter(Bitacora.fecha <= fecha_fin)

        campos_validos = {
            'fecha': Bitacora.fecha,
            'cliente': Bitacora.cliente,
            'empresa': Bitacora.empresa,
            'monto': Bitacora.monto
        }

        campo_orden = campos_validos.get(ordenar_por, Bitacora.fecha)

        if orden.lower() == "asc":
            query = query.order_by(campo_orden.asc())
        else:
            query = query.order_by(campo_orden.desc())

        return query.all()
