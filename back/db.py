import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener el entorno actual
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # Valor por defecto 'development'

if ENVIRONMENT == "production":
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
else:
    # Configuración mejorada para SQLite
    SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db?check_same_thread=False&mode=rwc"

# Motor de base de datos con configuración robusta
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Tiempo de espera mayor para operaciones
    },
    echo=True  # Mantén esto solo en desarrollo
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()