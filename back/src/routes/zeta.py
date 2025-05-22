from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import src.schemas.zeta_schema as zeta_schema
from src.repositories.zeta_repo import ZetaRepo
from src.repositories.id_zeta_repo import IdZetaRepo
import pandas as pd
from io import StringIO
from db import get_db

zeta = APIRouter(tags=["Zeta"])

@zeta.post("/zeta", response_model=zeta_schema.Zeta)
def create_zeta(zeta_data: zeta_schema.ZetaCreate, db: Session = Depends(get_db)):
    zeta_repo = ZetaRepo(db)
    id_zeta_repo = IdZetaRepo(db)
    id_zeta = id_zeta_repo.get_by_id(zeta_data.numero)
    if zeta_data.numero == 8:
        zeta_data.id_ocho = id_zeta.contador
    elif zeta_data.numero == 9:
        zeta_data.id_nueve = id_zeta.contador
    id_zeta_repo.modify_to_last_ticket(zeta_data.numero, zeta_data.ultimo_ticket)
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
            zeta.cuenta_corriente,
            zeta.gravado,
            "",
        ])

    csv_buffer = StringIO()
    df = pd.DataFrame(data)
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    filename = f"zetas_{fecha_inicio}_a_{fecha_fin}.csv"

    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
