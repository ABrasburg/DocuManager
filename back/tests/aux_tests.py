from db import Base, engine, SessionLocal

from src.models.comprobante  import Comprobante
from src.models.tipo_comprobante import TipoComprobante
from src.models.emisor import Emisor

def setup_module():
    """Preparar la base de datos para las pruebas"""
    db = SessionLocal()
    try:
        # Limpiar tablas antes de las pruebas
        db.query(Comprobante).delete()
        db.query(Emisor).delete()
        db.commit()
    finally:
        db.close()