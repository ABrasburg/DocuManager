from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Comprobante(Base):
    __tablename__ = "comprobante"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_emision = Column(String, nullable=False)
    punto_venta = Column(Integer, nullable=False)
    numero_desde = Column(Integer, nullable=False)
    numero_hasta = Column(Integer, nullable=False)
    cod_autorizacion = Column(Integer, nullable=False)
    tipo_cambio = Column(Float, nullable=False)
    moneda = Column(String, nullable=False)
    neto_gravado = Column(Float, nullable=False)
    neto_no_gravado = Column(Float)
    exento = Column(Float)
    otros_tributos = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    emisor_id = Column(Integer, ForeignKey("emisor.id"))
    emisor = relationship("Emisor", back_populates="comprobantes", lazy='joined')

    tipo_comprobante_id = Column(Integer, ForeignKey("tipo_comprobante.id"))
    tipo_comprobante = relationship("TipoComprobante", back_populates="comprobantes", lazy='joined')
