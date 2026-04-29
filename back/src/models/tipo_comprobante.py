from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base


class TipoComprobante(Base):
    __tablename__ = "tipo_comprobante"
    __table_args__ = (UniqueConstraint("tipo_comprobante", "farmacia_id"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_comprobante = Column(Integer, nullable=False)
    nombre = Column(String, nullable=False)
    farmacia_id = Column(Integer, ForeignKey("farmacia.id"), nullable=False)

    comprobantes = relationship("Comprobante", back_populates="tipo_comprobante")