from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from db import Base

class ArchivosComprobantes(Base):
    __tablename__ = "archivos_comprobantes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_archivo = Column(String, nullable=False)
    numero_hasta = Column(Integer, nullable=True)