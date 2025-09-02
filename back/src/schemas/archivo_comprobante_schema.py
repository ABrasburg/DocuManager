from pydantic import BaseModel, ConfigDict

class ArchivoComprobanteBase(BaseModel):
    nombre_archivo: str
    numero_hasta: int = None

class ArchivoComprobanteCreate(ArchivoComprobanteBase):
    pass

class ArchivoComprobante(ArchivoComprobanteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    