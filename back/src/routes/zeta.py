from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.zeta_schema as zeta_schema
import src.schemas.id_zeta_schema as id_zeta_schema
from src.repositories.zeta_repo import ZetaRepo
from src.repositories.id_zeta_repo import IdZetaRepo
from db import get_db

zeta = APIRouter(tags=["Zeta"])

@zeta.post("/zeta", response_model=zeta_schema.Zeta)
def create_zeta(zeta_data: zeta_schema.ZetaCreate, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    id_zeta_repo = IdZetaRepo(db)
    id_zeta = id_zeta_repo.get_by_id(zeta_data.punto_de_venta)
    if zeta_data.punto_de_venta == 8:
        zeta_data.id_ocho = id_zeta.contador
    elif zeta_data.punto_de_venta == 9:
        zeta_data.id_nueve = id_zeta.contador
    id_zeta_repo.sumar_contador(zeta_data.punto_de_venta)
    return zeta_repo.create_zeta(zeta_data)

@zeta.get("/zeta/{id}", response_model=zeta_schema.Zeta)
def get_zeta(id: int, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    db_zeta = zeta_repo.get_zeta(id)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta

@zeta.get("/zetas", response_model=List[zeta_schema.Zeta])
def get_zetas(db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    return zeta_repo.get_zetas()

@zeta.get("/zetas/fecha", response_model=List[zeta_schema.Zeta])
def get_zetas_by_fecha(fecha_desde: str, fecha_hasta: str, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    return zeta_repo.get_zetas_by_fecha(fecha_desde, fecha_hasta)

@zeta.get("/zetas/cuenta_corriente", response_model=List[zeta_schema.Zeta])
def get_zetas_by_cuenta_corriente(cuenta_corriente: str, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    return zeta_repo.get_zetas_by_cuenta_corriente(cuenta_corriente)

@zeta.delete("/zeta/{id}", response_model=zeta_schema.Zeta)
def delete_zeta(id: int, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    db_zeta = zeta_repo.delete_zeta(id)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta