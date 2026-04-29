from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import src.schemas.tipo_comprobante_schema as tipo_comprobante_schema
from src.repositories.tipo_comprobante_repo import TipoComprobanteRepo
from db import get_db

tipo_comprobante = APIRouter(tags=["Tipo de Comprobante"])


def get_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return TipoComprobanteRepo(db, farmacia_id)


@tipo_comprobante.get("/tipos_comprobantes", response_model=List[tipo_comprobante_schema.TipoComprobante])
def get_tipos_comprobantes(r: TipoComprobanteRepo = Depends(get_repo)):
    return r.get_tipos_comprobantes()


@tipo_comprobante.post("/tipo_comprobante", response_model=tipo_comprobante_schema.TipoComprobante, status_code=201)
def create_tipo_comprobante(tipo_comprobante: tipo_comprobante_schema.TipoComprobanteCreate, r: TipoComprobanteRepo = Depends(get_repo)):
    return r.create_tipo_comprobante(tipo_comprobante)


@tipo_comprobante.delete("/tipo_comprobante/{tipo_comprobante}", response_model=tipo_comprobante_schema.TipoComprobante)
def delete_tipo_comprobante(tipo_comprobante: int, r: TipoComprobanteRepo = Depends(get_repo)):
    return r.delete_tipo_comprobante(tipo_comprobante)


@tipo_comprobante.get("/tipo_comprobante/{tipo_comprobante}", response_model=tipo_comprobante_schema.TipoComprobante)
def existe_tipo_comprobante(tipo_comprobante: int, r: TipoComprobanteRepo = Depends(get_repo)):
    return r.existe_tipo_comprobante(tipo_comprobante)
