from sqlalchemy import Column, Integer, String, DateTime
from db import Base


class Zeta(Base):
    __tablename__ = "zeta"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    numero = Column(Integer, nullable=False)
    ultimo_ticket = Column(Integer, nullable=False)
    exento = Column(Integer, nullable=False)
    iva = Column(Integer, nullable=False)
    gravado = Column(Integer, nullable=False)
    cuenta_corriente = Column(String, nullable=False)
    total = Column(Integer, nullable=False)