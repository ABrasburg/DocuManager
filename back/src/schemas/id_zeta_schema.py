from pydantic import BaseModel, ConfigDict
from typing import Optional


class ZetaBase(BaseModel):
    id: int
    contador: Optional[int] = 0

class ZetaCreate(ZetaBase):
    pass

class Zeta(ZetaBase):
    pass