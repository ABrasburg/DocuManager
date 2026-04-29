from pydantic import BaseModel


class FarmaciaCreate(BaseModel):
    nombre: str


class Farmacia(FarmaciaCreate):
    id: int

    class Config:
        from_attributes = True
