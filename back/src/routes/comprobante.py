from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
import src.schemas.comprobante_schema as schemas
import src.repositories.comprobante_repo as repo
from src.repositories.tipo_comprobante_repo import TipoComprobanteRepo
from src.repositories.emisor_repo import EmisorRepo
from db import get_db

comprobante = APIRouter(tags=["Comprobante"])


@comprobante.get("/comprobantes", response_model=List[schemas.Comprobante])
def get_comprobantes(db: Session = Depends(get_db)):
    return repo.ComprobanteRepo(db).get_comprobantes()


@comprobante.post("/comprobante", response_model=schemas.Comprobante, status_code=201)
def create_comprobante(
    comprobante: schemas.ComprobanteCreate, db: Session = Depends(get_db)
):
    tipo_repo = TipoComprobanteRepo(db)
    db_tipo = tipo_repo.get_tipo_comprobante(
        comprobante.tipo_comprobante.tipo_comprobante
    )
    if not db_tipo:
        # Si no existe el tipo de comprobante no creo nada
        raise HTTPException(status_code=404, detail="Tipo de comprobante no encontrado")

    emisor_repo = EmisorRepo(db)
    db_emisor = emisor_repo.get_emisor(comprobante.emisor.cuit)
    if not db_emisor:
        db_emisor = emisor_repo.create_emisor(comprobante.emisor)

    comprobante_data = comprobante.model_dump()
    comprobante_data["emisor_id"] = db_emisor.id
    comprobante_data["tipo_comprobante_id"] = db_tipo.id

    comprobante_data.pop("emisor", None)
    comprobante_data.pop("tipo_comprobante", None)

    return repo.ComprobanteRepo(db).create_comprobante(comprobante_data)


@comprobante.delete("/comprobante/{id}", response_model=schemas.Comprobante)
def delete_comprobante(id: int, db: Session = Depends(get_db)):
    return repo.ComprobanteRepo(db).delete_comprobante(id)


@comprobante.get("/comprobante/{id}", response_model=schemas.Comprobante)
def get_comprobante(id: int, db: Session = Depends(get_db)):
    return repo.ComprobanteRepo(db).get_comprobante(id)


@comprobante.get(
    "/comprobantes/emisor/{cuit}", response_model=List[schemas.Comprobante]
)
def get_comprobantes_by_emisor(cuit: int, db: Session = Depends(get_db)):
    return repo.ComprobanteRepo(db).get_comprobantes_by_emisor(cuit)


@comprobante.get(
    "/comprobantes/tipo_comprobante/{tipo_comprobante}",
    response_model=List[schemas.Comprobante],
)
def get_comprobantes_by_tipo_comprobante(
    tipo_comprobante: int, db: Session = Depends(get_db)
):
    return repo.ComprobanteRepo(db).get_comprobantes_by_tipo_comprobante(
        tipo_comprobante
    )


@comprobante.get("/comprobantes/fechas", response_model=List[schemas.Comprobante])
def get_comprobantes_by_fechas(
    fecha_inicio: str, fecha_fin: str, db: Session = Depends(get_db)
):
    return repo.ComprobanteRepo(db).get_comprobantes_by_fechas(fecha_inicio, fecha_fin)


@comprobante.get("/comprobantes/filtering", response_model=List[schemas.Comprobante])
def get_comprobante_filtering(
    cuit: int,
    tipo_comprobante: int,
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    return repo.ComprobanteRepo(db).get_comprobante_filtering(
        cuit, tipo_comprobante, fecha_inicio, fecha_fin
    )


@comprobante.post("/comprobantes/upload")
async def upload_comprobantes(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Importa comprobantes desde un archivo CSV.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, detail="Solo se permiten archivos CSV")

    try:
        contents = await file.read()
        content_str = contents.decode('utf-8-sig')
        
        df = pd.read_csv(
            StringIO(content_str),
            sep=';',
            decimal=',',
            quotechar='"',
            engine='python',
            on_bad_lines='warn'
        )

        required_columns = {
            "Fecha de Emisión",
            "Tipo de Comprobante",
            "Punto de Venta",
            "Número Desde",
            "Número Hasta",
            "Cód. Autorización",
            "Tipo Doc. Emisor",
            "Nro. Doc. Emisor",
            "Denominación Emisor",
            "Tipo Cambio",
            "Moneda",
            "Imp. Neto Gravado",
            "Imp. Neto No Gravado",
            "Imp. Op. Exentas",
            "IVA",
            "Imp. Total",
        }
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise HTTPException(
                status_code=400,
                detail=f"El archivo CSV no tiene las columnas requeridas. Faltan: {missing}",
            )

        resultados = []
        for index, row in df.iterrows():
            try:
                comprobante_data = schemas.ComprobanteCreate(
                    fecha_emision=row["Fecha de Emisión"],
                    punto_venta=int(row["Punto de Venta"]),
                    numero_desde=int(row["Número Desde"]),
                    numero_hasta=int(row["Número Hasta"]),
                    cod_autorizacion=int(row["Cód. Autorización"]),
                    tipo_cambio=float(row["Tipo Cambio"]),
                    moneda=row["Moneda"],
                    neto_gravado=float(row["Imp. Neto Gravado"]),
                    neto_no_gravado=float(row["Imp. Neto No Gravado"]),
                    exento=float(row["Imp. Op. Exentas"]),
                    otros_tributos=float(row["Otros Tributos"]),
                    iva=float(row["IVA"]),
                    total=float(row["Imp. Total"]),
                    emisor=schemas.EmisorCreate(
                        cuit=row["Nro. Doc. Emisor"],
                        denominacion=row["Denominación Emisor"],
                        tipo_doc=str(row["Tipo Doc. Emisor"]),
                    ),
                    tipo_comprobante=schemas.TipoComprobanteCreate(
                        tipo_comprobante=int(row["Tipo de Comprobante"]),
                        nombre=f"Tipo-{int(row["Tipo de Comprobante"])}", # Si no existe igual no lo crea
                    ),
                )

                response = create_comprobante(comprobante_data, db)

            except HTTPException as e:
                resultados.append(
                    {"fila": index + 1, "estado": "error", "error": e.detail}
                )
            except Exception as e:
                resultados.append(
                    {"fila": index + 1, "estado": "error", "error": str(e)}
                )

        exitos = sum(1 for r in resultados if r["estado"] == "éxito")
        errores = len(resultados) - exitos

        return {
            "mensaje": f"Procesado completo. Éxitos: {exitos}, Errores: {errores}",
            "detalles": resultados,
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(400, detail="El archivo CSV está vacío")
    except pd.errors.ParserError:
        raise HTTPException(400, detail="El archivo CSV no tiene un formato válido")
    except Exception as e:
        raise HTTPException(500, detail=f"Error al procesar el archivo: {str(e)}")
