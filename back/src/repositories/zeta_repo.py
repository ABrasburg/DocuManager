from sqlalchemy.orm import Session
from datetime import datetime

from src.models.zeta import Zeta
from src.schemas.zeta_schema import ZetaCreate


class ZetaRepo:
    def __init__(self, db: Session, farmacia_id: int):
        self.db = db
        self.farmacia_id = farmacia_id

    def create_zeta(self, zeta: ZetaCreate):
        db_zeta = Zeta(**zeta.model_dump(), farmacia_id=self.farmacia_id)
        self.db.add(db_zeta)
        self.db.commit()
        self.db.refresh(db_zeta)
        return db_zeta

    def get_zeta(self, id: int):
        return self.db.query(Zeta).filter(Zeta.id == id, Zeta.farmacia_id == self.farmacia_id).first()

    def get_zetas(self):
        return self.db.query(Zeta).filter(Zeta.farmacia_id == self.farmacia_id).all()

    def _parse_fecha(self, fecha: str):
        for formato in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(fecha, formato)
            except ValueError:
                continue
        raise ValueError("Formato de fecha invalido. Use YYYY-MM-DD o DD/MM/YYYY")

    def get_zetas_by_fecha(self, fecha_desde: str, fecha_hasta: str):
        fi = self._parse_fecha(fecha_desde)
        ff = self._parse_fecha(fecha_hasta).replace(hour=23, minute=59, second=59)
        return self.db.query(Zeta).filter(
            Zeta.farmacia_id == self.farmacia_id,
            Zeta.fecha >= fi,
            Zeta.fecha <= ff,
        ).all()

    def update_zeta(self, id: int, zeta: ZetaCreate):
        db_zeta = self.get_zeta(id)
        if db_zeta:
            for key, value in zeta.model_dump().items():
                setattr(db_zeta, key, value)
            self.db.commit()
            self.db.refresh(db_zeta)
        return db_zeta

    def delete_zeta(self, id: int):
        db_zeta = self.get_zeta(id)
        if db_zeta:
            self.db.delete(db_zeta)
            self.db.commit()
        return db_zeta
