from pydantic import BaseModel, ConfigDict
from src.schemas.emisor_schema import Emisor, EmisorCreate
from src.schemas.tipo_comprobante_schema import TipoComprobante, TipoComprobanteCreate
from  typing import Optional

class ComprobanteBase(BaseModel):
    fecha_emision: str
    punto_venta: int
    numero_desde: int
    numero_hasta: int
    cod_autorizacion: int
    tipo_cambio: float
    moneda: str
    neto_gravado: float
    neto_no_gravado: Optional[float]
    exento: Optional[float]
    otros_tributos: float
    iva: float
    total: float
    fecha_pago: Optional[str] = None
    numero_ticket: Optional[str] = None

class ComprobanteCreate(ComprobanteBase):
    emisor: EmisorCreate
    tipo_comprobante: TipoComprobanteCreate 

class ComprobantePago(BaseModel):
    fecha_pago: str
    numero_ticket: str

class Comprobante(ComprobanteBase):
    id: int
    emisor: Emisor
    tipo_comprobante: TipoComprobante
    model_config = ConfigDict(from_attributes=True)