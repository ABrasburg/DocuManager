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


def get_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return ZetaRepo(db, farmacia_id)


@zeta.post("/zeta", response_model=zeta_schema.Zeta)
def create_zeta(zeta_data: zeta_schema.ZetaCreate, r: ZetaRepo = Depends(get_repo)):
    return r.create_zeta(zeta_data)


@zeta.get("/zeta/{id}", response_model=zeta_schema.Zeta)
def get_zeta(id: int, r: ZetaRepo = Depends(get_repo)):
    db_zeta = r.get_zeta(id)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta


@zeta.get("/zetas", response_model=List[zeta_schema.Zeta])
def get_zetas(r: ZetaRepo = Depends(get_repo)):
    return r.get_zetas()


@zeta.get("/zetas/fecha", response_model=List[zeta_schema.Zeta])
def get_zetas_by_fecha(fecha_desde: str, fecha_hasta: str, r: ZetaRepo = Depends(get_repo)):
    return r.get_zetas_by_fecha(fecha_desde, fecha_hasta)


@zeta.put("/zeta/{id}", response_model=zeta_schema.Zeta)
def update_zeta(id: int, zeta_data: zeta_schema.ZetaCreate, r: ZetaRepo = Depends(get_repo)):
    db_zeta = r.update_zeta(id, zeta_data)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta


@zeta.delete("/zeta/{id}", response_model=zeta_schema.Zeta)
def delete_zeta(id: int, r: ZetaRepo = Depends(get_repo)):
    db_zeta = r.delete_zeta(id)
    if not db_zeta:
        raise HTTPException(status_code=404, detail="Zeta not found")
    return db_zeta


@zeta.get("/zetas/download")
async def download_zetas(fecha_inicio: str, fecha_fin: str, r: ZetaRepo = Depends(get_repo)):
    zetas = r.get_zetas_by_fecha(fecha_inicio, fecha_fin)
    if not zetas:
        raise HTTPException(status_code=404, detail="No se encontraron zetas para las fechas proporcionadas.")

    data = [{
        "Fecha": z.fecha.strftime("%d/%m/%Y"),
        "Punto de Venta": z.punto_de_venta,
        "Número": z.numero,
        "Último Ticket": z.ultimo_ticket,
        "Exento": z.exento,
        "IVA": z.iva,
        "Perfumería": z.perfumeria,
        "Medicamentos IVA": z.medicamentos_iva,
        "Total": z.total,
    } for z in zetas]

    csv_buffer = StringIO()
    fieldnames = ["Fecha", "Punto de Venta", "Número", "Último Ticket", "Exento", "IVA", "Perfumería", "Medicamentos IVA", "Total"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for row in data:
        formatted = {
            k: str(v).replace('.', ',') if isinstance(v, float) else v
            for k, v in row.items()
        }
        writer.writerow(formatted)

    csv_buffer.seek(0)
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=zetas_{fecha_inicio}_a_{fecha_fin}.csv"}
    )
