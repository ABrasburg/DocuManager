from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base


class TipoComprobante(Base):
    __tablename__ = "tipo_comprobante"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_comprobante = Column(Integer, unique=True, nullable=False)
    nombre = Column(String, nullable=False)

    comprobantes = relationship("Comprobante", back_populates="tipo_comprobante")