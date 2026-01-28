import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bitacora_model import Base
import urllib.parse

load_dotenv()

params = urllib.parse.quote_plus(
    f"DRIVER={{{os.environ.get('SQL_SERVER_DRIVER')}}};"
    f"SERVER={os.environ.get('SQL_SERVER_HOST')};"
    f"DATABASE={os.environ.get('SQL_SERVER_DATABASE')};"
    f"Trusted_Connection={os.environ.get('SQL_TRUSTED_CONNECTION')};"
)
URL_DATABASE = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(URL_DATABASE, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Provee sesión de base de datos con gestión automática de ciclo de vida"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Ejecuta DDL para creación de esquema de base de datos"""
    Base.metadata.create_all(bind=engine)
