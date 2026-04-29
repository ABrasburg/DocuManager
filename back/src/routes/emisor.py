from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.emisor_schema as schemas
import src.repositories.emisor_repo as repo
from db import get_db

emisor = APIRouter(tags=["Emisor"])


def get_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return repo.EmisorRepo(db, farmacia_id)


@emisor.get("/emisores", response_model=List[schemas.Emisor])
def get_emisores(r: repo.EmisorRepo = Depends(get_repo)):
    return r.get_emisores()


@emisor.post("/emisor", response_model=schemas.Emisor, status_code=201)
def create_emisor(emisor: schemas.EmisorCreate, r: repo.EmisorRepo = Depends(get_repo)):
    return r.create_emisor(emisor)


@emisor.delete("/emisor/{cuit}", response_model=schemas.Emisor)
def delete_emisor(cuit: int, r: repo.EmisorRepo = Depends(get_repo)):
    return r.delete_emisor(cuit)


@emisor.get("/emisor/{cuit}", response_model=schemas.Emisor)
def existe_emisor(cuit: int, r: repo.EmisorRepo = Depends(get_repo)):
    return r.get_emisor(cuit)


@emisor.put("/emisor/{cuit}", response_model=schemas.Emisor)
def update_emisor(cuit: int, emisor: schemas.EmisorCreate, r: repo.EmisorRepo = Depends(get_repo)):
    db_emisor = r.get_emisor(cuit)
    if not db_emisor:
        raise HTTPException(status_code=404, detail="Emisor not found")
    return r.update_emisor(cuit, emisor)


@emisor.put("/emisor/{cuit}/cuenta_corriente", response_model=schemas.Emisor)
def set_cuenta_corriente(cuit: int, cuenta_corriente: bool, r: repo.EmisorRepo = Depends(get_repo)):
    db_emisor = r.get_emisor(cuit)
    if not db_emisor:
        raise HTTPException(status_code=404, detail="Emisor not found")
    return r.set_cuenta_corriente(cuit, cuenta_corriente)
