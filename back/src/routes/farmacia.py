from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.farmacia_schema as schemas
from src.repositories.farmacia_repo import FarmaciaRepo
from db import get_db

farmacia = APIRouter(tags=["Farmacia"])


@farmacia.get("/farmacias", response_model=List[schemas.Farmacia])
def get_farmacias(db: Session = Depends(get_db)):
    return FarmaciaRepo(db).get_farmacias()


@farmacia.post("/farmacia", response_model=schemas.Farmacia, status_code=201)
def create_farmacia(farmacia: schemas.FarmaciaCreate, db: Session = Depends(get_db)):
    return FarmaciaRepo(db).create_farmacia(farmacia)
