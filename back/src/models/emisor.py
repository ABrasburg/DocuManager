from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from db import Base


class Emisor(Base):
    __tablename__ = "emisor"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_doc = Column(String, nullable=False)
    cuit = Column(Integer, unique=True, nullable=False)
    denominacion = Column(String, nullable=False)

    comprobantes = relationship("Comprobante", back_populates="emisor")