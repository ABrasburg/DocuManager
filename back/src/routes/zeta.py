from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import src.schemas.zeta_schema as zeta_schema
from src.repositories.zeta_repo import ZetaRepo
import csv
from io import StringIO
from db import get_db

zeta = APIRouter(tags=["Zeta"])

@zeta.post("/zeta", response_model=zeta_schema.Zeta)
def create_zeta(zeta_data: zeta_schema.ZetaCreate, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
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

@zeta.delete("/zeta/{id}", response_model=zeta_schema.Zeta)
def delete_zeta(id: int, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    db_zeta = zeta_repo.delete_zeta(id)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta

@zeta.get("/zetas/download")
async def download_zetas(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    """
    Descarga las zetas filtrados por fechas en formato CSV.
    """
    zetas = ZetaRepo(db).get_zetas_by_fecha(
        fecha_inicio, fecha_fin
    )
    if not zetas:
        raise HTTPException(status_code=404, detail="No se encontraron zetas para las fechas proporcionadas.")
    
    data = []
    for zeta in zetas:
        data.append([
           zeta.fecha.strftime("%d/%m/%Y"),
            f"Z-{zeta.numero:05d}",
            max(zeta.id_ocho or "", zeta.id_nueve or ""),
            f"Z-{zeta.numero:05d}",
            zeta.ultimo_ticket,
            1,
            "Consumidos final",
            0,
            zeta.total,
            zeta.exento,
            zeta.medicamentos_iva,
            zeta.perfumeria,
            "",
        ])

    csv_buffer = StringIO()
    if data:
        # Escribir CSV sin headers (como estaba con pandas)
        writer = csv.writer(csv_buffer)
        writer.writerows(data)
    csv_buffer.seek(0)
    filename = f"zetas_{fecha_inicio}_a_{fecha_fin}.csv"

    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
