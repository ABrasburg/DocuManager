from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.schemas.archivo_comprobante_schema as schemas
import src.repositories.archivo_comprobante_repo as repo
from db import get_db

archivo_comprobante = APIRouter(tags=["Archivo Comprobante"])

@archivo_comprobante.post("/archivo_comprobante", response_model=schemas.ArchivoComprobante)
def create_archivo_comprobante(
    archivo_comprobante: schemas.ArchivoComprobanteCreate,
    db: Session = Depends(get_db),
):
    archivo_comprobante_repo = repo.ArchivoComprobanteRepo(db)
    if archivo_comprobante_repo.exists_archivo_comprobante(archivo_comprobante.nombre_archivo):
        raise HTTPException(status_code=400, detail="El archivo ya existe")
    
    return archivo_comprobante_repo.create_archivo_comprobante(archivo_comprobante)