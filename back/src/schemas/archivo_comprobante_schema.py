from pydantic import BaseModel, ConfigDict

class ArchivoComprobanteBase(BaseModel):
    nombre_archivo: str

class ArchivoComprobanteCreate(ArchivoComprobanteBase):
    pass

class ArchivoComprobante(ArchivoComprobanteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    