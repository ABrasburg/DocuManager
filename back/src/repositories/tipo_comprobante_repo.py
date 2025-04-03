from sqlalchemy.orm import Session

from src.models.tipo_comprobante import TipoComprobante
from src.schemas.tipo_comprobante_schema import TipoComprobanteCreate


class TipoComprobanteRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_tipos_comprobantes(self):
        return self.db.query(TipoComprobante).all()

    def get_tipo_comprobante(self, tipo_comprobante: int):
        return (
            self.db.query(TipoComprobante)
            .filter(TipoComprobante.tipo_comprobante == tipo_comprobante)
            .first()
        )

    def create_tipo_comprobante(self, tipo_comprobante: TipoComprobanteCreate):
        db_tipo_comprobante = TipoComprobante(**tipo_comprobante.model_dump())
        self.db.add(db_tipo_comprobante)
        self.db.commit()
        self.db.refresh(db_tipo_comprobante)
        return db_tipo_comprobante

    def delete_tipo_comprobante(self, tipo_comprobante: int):
        db_tipo_comprobante = (
            self.db.query(TipoComprobante)
            .filter(TipoComprobante.tipo_comprobante == tipo_comprobante)
            .first()
        )
        self.db.delete(db_tipo_comprobante)
        self.db.commit()
        return db_tipo_comprobante
