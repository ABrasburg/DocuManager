from sqlalchemy import Column, Integer, DateTime, Float
from db import Base


class Zeta(Base):
    __tablename__ = "zeta"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_ocho = Column(Integer, default=-1)
    id_nueve = Column(Integer, default=-1)
    fecha = Column(DateTime, nullable=False)
    punto_de_venta = Column(Integer, nullable=False)
    numero = Column(Integer, nullable=False)
    ultimo_ticket = Column(Integer, nullable=False)
    exento = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    gravado = Column(Float, nullable=False)
    cuenta_corriente = Column(Float, nullable=False)
    total = Column(Float, nullable=False)