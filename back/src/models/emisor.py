from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base


class Emisor(Base):
    __tablename__ = "emisor"
    __table_args__ = (UniqueConstraint("cuit", "farmacia_id"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_doc = Column(String, nullable=False)
    cuit = Column(Integer, nullable=False)
    denominacion = Column(String, nullable=False)
    cuenta_corriente = Column(Boolean, nullable=False)
    farmacia_id = Column(Integer, ForeignKey("farmacia.id"), nullable=False)

    comprobantes = relationship("Comprobante", back_populates="emisor")