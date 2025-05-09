from sqlalchemy.orm import Session
from fastapi import HTTPException

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
    
    def update_comprobante(self, id: int, comprobante: ComprobanteCreate):
        db_comprobante = self.db.query(Comprobante).filter(Comprobante.id == id).first()
        if db_comprobante is None:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        for key, value in comprobante.items():
            setattr(db_comprobante, key, value)
        self.db.commit()
        self.db.refresh(db_comprobante)
        return db_comprobante
    
    def delete_comprobante(self, id: int):
        db_comprobante = self.db.query(Comprobante).filter(Comprobante.id == id).first()
        if db_comprobante is None:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        self.db.delete(db_comprobante)
        self.db.commit()
        return db_comprobante
    
    def get_comprobantes_by_tipo_comprobante(self, tipo_comprobante: int):
        return self.db.query(Comprobante).filter(Comprobante.tipo_comprobante == tipo_comprobante).all()
    
    def get_comprobantes_by_fechas(self, fecha_inicio: str, fecha_fin: str):
        return self.db.query(Comprobante).filter(Comprobante.fecha_emision >= fecha_inicio, Comprobante.fecha_emision <= fecha_fin).all()
    
    def get_comprobantes_by_emisor_and_fechas(self, emisor_id: int, fecha_inicio: str, fecha_fin: str):
        return self.db.query(Comprobante).filter(Comprobante.emisor_id == emisor_id, Comprobante.fecha_emision >= fecha_inicio, Comprobante.fecha_emision <= fecha_fin).all()