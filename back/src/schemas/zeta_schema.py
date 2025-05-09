from pydantic import BaseModel, ConfigDict
from datetime import datetime
from  typing import Optional


class ZetaBase(BaseModel):
    fecha: datetime
    numero: int
    punto_de_venta: int
    id_ocho: Optional[int] = -1
    id_nueve: Optional[int] = -1
    ultimo_ticket: int
    exento: float
    iva: float
    gravado: float
    cuenta_corriente: float
    total: float

class ZetaCreate(ZetaBase):
    pass

class Zeta(ZetaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)