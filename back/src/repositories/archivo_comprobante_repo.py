from sqlalchemy.orm import Session

from src.models.archivos_comprobantes import ArchivosComprobantes
from src.schemas.archivo_comprobante_schema import ArchivoComprobanteCreate

class ArchivoComprobanteRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_archivo_comprobante(self, archivo_comprobante: ArchivoComprobanteCreate):
        db_archivo_comprobante = ArchivosComprobantes(**archivo_comprobante.model_dump())
        self.db.add(db_archivo_comprobante)
        self.db.commit()
        self.db.refresh(db_archivo_comprobante)
        return db_archivo_comprobante
    
    def get_archivo_comprobante(self, archivo_comprobante_nombre: str):
        return self.db.query(ArchivosComprobantes).filter(ArchivosComprobantes.nombre_archivo == archivo_comprobante_nombre).first()

    def exists_archivo_comprobante(self, nombre_archivo: str):
        return self.db.query(ArchivosComprobantes).filter(ArchivosComprobantes.nombre_archivo == nombre_archivo).first() is not None