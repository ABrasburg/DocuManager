from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.id_zeta import IdZeta
from src.schemas.id_zeta_schema import ZetaCreate

class IdZetaRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_id_zeta(self):
        return self.db.query(IdZeta).first()
    
    def create_id_zeta(self, id_zeta: ZetaCreate):
        db_id_zeta = IdZeta(**id_zeta)
        self.db.add(db_id_zeta)
        self.db.commit()
        self.db.refresh(db_id_zeta)
        return db_id_zeta