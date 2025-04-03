from sqlalchemy.orm import Session

from src.models.comprobante import Comprobante
from src.schemas.comprobante_schema import ComprobanteCreate


class ComprobanteRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_comprobantes(self):
        return self.db.query(Comprobante).all()
    
    def get_comprobante(self, id: int):
        return self.db.query(Comprobante).filter(Comprobante.id == id).first()
    
    def create_comprobante(self, comprobante: ComprobanteCreate):
        db_comprobante = Comprobante(**comprobante)
        self.db.add(db_comprobante)
        self.db.commit()
        self.db.refresh(db_comprobante)
        return db_comprobante
    
    def delete_comprobante(self, id: int):
        db_comprobante = self.db.query(Comprobante).filter(Comprobante.id == id).first()
        self.db.delete(db_comprobante)
        self.db.commit()
        return db_comprobante
    
    def get_comprobantes_by_emisor(self, cuit: int):
        return self.db.query(Comprobante).filter(Comprobante.cuit == cuit).all()
    
    def get_comprobantes_by_tipo_comprobante(self, tipo_comprobante: int):
        return self.db.query(Comprobante).filter(Comprobante.tipo_comprobante == tipo_comprobante).all()
    
    def get_comprobantes_by_fechas(self, fecha_inicio: str, fecha_fin: str):
        return self.db.query(Comprobante).filter(Comprobante.fecha >= fecha_inicio, Comprobante.fecha <= fecha_fin).all()
    
    def get_comprobante_filtering(self, cuit: int, tipo_comprobante: int, fecha_inicio: str, fecha_fin: str):
        return self.db.query(Comprobante).filter(Comprobante.cuit == cuit, Comprobante.tipo_comprobante == tipo_comprobante, Comprobante.fecha >= fecha_inicio, Comprobante.fecha <= fecha_fin).all()