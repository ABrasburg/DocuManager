from sqlalchemy.orm import Session

from src.models.tipo_comprobante import TipoComprobante
from src.schemas.tipo_comprobante_schema import TipoComprobanteCreate


class TipoComprobanteRepo:
    def __init__(self, db: Session, farmacia_id: int):
        self.db = db
        self.farmacia_id = farmacia_id

    def get_tipos_comprobantes(self):
        return self.db.query(TipoComprobante).filter(TipoComprobante.farmacia_id == self.farmacia_id).all()

    def get_tipo_comprobante(self, tipo_comprobante: int):
        return self.db.query(TipoComprobante).filter(
            TipoComprobante.tipo_comprobante == tipo_comprobante,
            TipoComprobante.farmacia_id == self.farmacia_id
        ).first()

    def create_tipo_comprobante(self, tipo_comprobante: TipoComprobanteCreate):
        db_tipo = TipoComprobante(**tipo_comprobante.model_dump(), farmacia_id=self.farmacia_id)
        self.db.add(db_tipo)
        self.db.commit()
        self.db.refresh(db_tipo)
        return db_tipo

    def delete_tipo_comprobante(self, tipo_comprobante: int):
        db_tipo = self.get_tipo_comprobante(tipo_comprobante)
        self.db.delete(db_tipo)
        self.db.commit()
        return db_tipo

    def existe_tipo_comprobante(self, tipo_comprobante: int):
        return self.get_tipo_comprobante(tipo_comprobante)
