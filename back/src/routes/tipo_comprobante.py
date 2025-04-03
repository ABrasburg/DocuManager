from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.tipo_comprobante_schema as tipo_comprobante_schema
from src.repositories.tipo_comprobante_repo import TipoComprobanteRepo
from db import get_db

tipo_comprobante = APIRouter(tags=["Tipo de Comprobante"])


@tipo_comprobante.get(
    "/tipos_comprobantes", response_model=List[tipo_comprobante_schema.TipoComprobante]
)
def get_tipos_comprobantes(db: Session = Depends(get_db)):
    return TipoComprobanteRepo(db).get_tipos_comprobantes()


@tipo_comprobante.post(
    "/tipo_comprobante",
    response_model=tipo_comprobante_schema.TipoComprobante,
    status_code=201,
)
def create_tipo_comprobante(
    tipo_comprobante: tipo_comprobante_schema.TipoComprobanteCreate,
    db: Session = Depends(get_db),
):
    return TipoComprobanteRepo(db).create_tipo_comprobante(tipo_comprobante)


@tipo_comprobante.delete(
    "/tipo_comprobante/{tipo_comprobante}",
    response_model=tipo_comprobante_schema.TipoComprobante,
)
def delete_tipo_comprobante(tipo_comprobante: int, db: Session = Depends(get_db)):
    return TipoComprobanteRepo(db).delete_tipo_comprobante(tipo_comprobante)


@tipo_comprobante.get(
    "/tipo_comprobante/{tipo_comprobante}",
    response_model=tipo_comprobante_schema.TipoComprobante,
)
def existe_tipo_comprobante(tipo_comprobante: int, db: Session = Depends(get_db)):
    return TipoComprobanteRepo(db).existe_tipo_comprobante(tipo_comprobante)
