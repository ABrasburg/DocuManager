import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener el entorno actual
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # Valor por defecto 'development'

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db?check_same_thread=False&mode=rwc")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    echo=ENVIRONMENT != "production",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()