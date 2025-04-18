from pydantic import BaseModel, ConfigDict


class EmisorBase(BaseModel):
    cuit: int
    tipo_doc: str
    denominacion: str


class EmisorCreate(EmisorBase):
    pass


class Emisor(EmisorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
