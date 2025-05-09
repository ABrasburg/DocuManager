from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.id_zeta import IdZeta
from src.schemas.id_zeta_schema import ZetaCreate

class IdZetaRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int):
        id_zeta = self.db.query(IdZeta).filter(IdZeta.id == id).first()
        if not id_zeta:
            raise HTTPException(status_code=404, detail="IdZeta not found")
        return id_zeta
    
    def create_id_zeta(self, id_zeta: ZetaCreate):
        db_id_zeta = IdZeta(**id_zeta)
        self.db.add(db_id_zeta)
        self.db.commit()
        self.db.refresh(db_id_zeta)
        return db_id_zeta
    
    def sumar_contador(self, id: int):
        id_zeta = self.db.query(IdZeta).filter(IdZeta.id == id).first()
        if not id_zeta:
            raise HTTPException(status_code=404, detail="IdZeta not found")
        id_zeta.contador += 1
        self.db.commit()
        self.db.refresh(id_zeta)
        return id_zeta