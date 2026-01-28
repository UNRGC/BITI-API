from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Bitacora(Base):
    """Entidad ORM para tabla de registros"""
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.datetime.now)
    cliente = Column(String)
    empresa = Column(String, default="Desconocido")
    poliza = Column(Boolean, default=False)
    problema = Column(String)
    solucion = Column(String)
    monto = Column(Float, default=0.0)
