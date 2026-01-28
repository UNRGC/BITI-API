import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bitacora_model import Base
import urllib.parse

load_dotenv()

# Determinar si usar autenticación SQL o Windows
trusted_connection = os.environ.get('SQL_TRUSTED_CONNECTION', 'no').lower()

if trusted_connection == 'yes':
    # Windows Authentication
    params = urllib.parse.quote_plus(
        f"DRIVER={{{os.environ.get('SQL_SERVER_DRIVER')}}};"
        f"SERVER={os.environ.get('SQL_SERVER_HOST')};"
        f"DATABASE={os.environ.get('SQL_SERVER_DATABASE')};"
        f"Trusted_Connection=yes;"
    )
    URL_DATABASE = f"mssql+pyodbc:///?odbc_connect={params}"
else:
    # SQL Server Authentication (para Docker)
    user = os.environ.get('SQL_SERVER_USER')
    password = os.environ.get('SQL_SERVER_PASSWORD')
    params = urllib.parse.quote_plus(
        f"DRIVER={{{os.environ.get('SQL_SERVER_DRIVER')}}};"
        f"SERVER={os.environ.get('SQL_SERVER_HOST')};"
        f"DATABASE={os.environ.get('SQL_SERVER_DATABASE')};"
        f"UID={user};"
        f"PWD={password};"
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
