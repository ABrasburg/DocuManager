from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ZetaBase(BaseModel):
    fecha: datetime
    numero: int
    ultimo_ticket: int
    exento: int
    iva: int
    gravado: int
    cuenta_corriente: str
    total: int

class ZetaCreate(ZetaBase):
    pass

class Zeta(ZetaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)