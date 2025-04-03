from pydantic import BaseModel, ConfigDict


class TipoComprobanteBase(BaseModel):
    tipo_comprobante: int
    nombre: str


class TipoComprobanteCreate(TipoComprobanteBase):
    pass


class TipoComprobante(TipoComprobanteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
