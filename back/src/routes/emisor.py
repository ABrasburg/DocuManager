from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.emisor_schema as schemas
import src.repositories.emisor_repo as repo
from db import get_db

emisor = APIRouter(tags=["Emisor"])


@emisor.get("/emisores", response_model=List[schemas.Emisor])
def get_emisores(db: Session = Depends(get_db)):
    return repo.EmisorRepo(db).get_emisores()


@emisor.post("/emisor", response_model=schemas.Emisor, status_code=201)
def create_emisor(emisor: schemas.EmisorCreate, db: Session = Depends(get_db)):
    return repo.EmisorRepo(db).create_emisor(emisor)


@emisor.delete("/emisor/{cuit}", response_model=schemas.Emisor)
def delete_emisor(cuit: int, db: Session = Depends(get_db)):
    return repo.EmisorRepo(db).delete_emisor(cuit)


@emisor.get("/emisor/{cuit}", response_model=schemas.Emisor)
def existe_emisor(cuit: int, db: Session = Depends(get_db)):
    return repo.EmisorRepo(db).get_emisor(cuit)
