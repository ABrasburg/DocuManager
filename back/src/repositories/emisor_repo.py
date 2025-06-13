from sqlalchemy.orm import Session

from src.models.emisor import Emisor
from src.schemas.emisor_schema import EmisorCreate


class EmisorRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_emisores(self):
        return self.db.query(Emisor).all()

    def get_emisor(self, cuit: int):
        return self.db.query(Emisor).filter(Emisor.cuit == cuit).first()
    
    def get_emisor_by_cuit(self, cuit: int):
        return self.db.query(Emisor).filter(Emisor.cuit == cuit).first()

    def create_emisor(self, emisor: EmisorCreate):
        db_emisor = Emisor(**emisor.model_dump())
        self.db.add(db_emisor)
        self.db.commit()
        self.db.refresh(db_emisor)
        return db_emisor

    def delete_emisor(self, cuit: int):
        db_emisor = self.db.query(Emisor).filter(Emisor.cuit == cuit).first()
        self.db.delete(db_emisor)
        self.db.commit()
        return db_emisor
    
    def update_emisor(self, cuit: int, emisor: EmisorCreate):
        db_emisor = self.db.query(Emisor).filter(Emisor.cuit == cuit).first()
        for key, value in emisor.model_dump().items():
            setattr(db_emisor, key, value)
        self.db.commit()
        self.db.refresh(db_emisor)
        return db_emisor
    
    def set_cuenta_corriente(self, cuit: int, cuenta_corriente: bool):
        db_emisor = self.db.query(Emisor).filter(Emisor.cuit == cuit).first()
        db_emisor.cuenta_corriente = cuenta_corriente
        self.db.commit()
        self.db.refresh(db_emisor)
        return db_emisor
