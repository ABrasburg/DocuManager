from sqlalchemy.orm import Session

from src.models.zeta import Zeta
from src.schemas.zeta_schema import ZetaCreate

class ZetaRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_zeta(self, zeta: ZetaCreate):
        db_zeta = Zeta(**zeta.model_dump())
        self.db.add(db_zeta)
        self.db.commit()
        self.db.refresh(db_zeta)
        return db_zeta
    
    def get_zeta(self, id: int):
        return self.db.query(Zeta).filter(Zeta.id == id).first()
    
    def get_zetas(self):
        return self.db.query(Zeta).all()
    
    def get_zetas_by_fecha(self, fecha_desde: str, fecha_hasta: str):
        return (
            self.db.query(Zeta)
            .filter(Zeta.fecha.between(fecha_desde, fecha_hasta))
            .all()
        )

    def get_zetas_by_cuenta_corriente(self, cuenta_corriente: str):
        return (
            self.db.query(Zeta)
            .filter(Zeta.cuenta_corriente == cuenta_corriente)
            .all()
        )

    def delete_zeta(self, id: int):
        db_zeta = self.db.query(Zeta).filter(Zeta.id == id).first()
        if db_zeta:
            self.db.delete(db_zeta)
            self.db.commit()
            return db_zeta
        return None