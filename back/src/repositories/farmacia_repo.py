from sqlalchemy.orm import Session
from src.models.farmacia import Farmacia
from src.schemas.farmacia_schema import FarmaciaCreate


class FarmaciaRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_farmacias(self):
        return self.db.query(Farmacia).all()

    def get_farmacia(self, farmacia_id: int):
        return self.db.query(Farmacia).filter(Farmacia.id == farmacia_id).first()

    def create_farmacia(self, farmacia: FarmaciaCreate):
        db_farmacia = Farmacia(**farmacia.model_dump())
        self.db.add(db_farmacia)
        self.db.commit()
        self.db.refresh(db_farmacia)
        return db_farmacia
