from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
import src.schemas.comprobante_schema as schemas
import src.repositories.comprobante_repo as repo
from src.repositories.tipo_comprobante_repo import TipoComprobanteRepo
from src.routes.archivo_comprobante import create_archivo_comprobante
from src.schemas.archivo_comprobante_schema import ArchivoComprobanteCreate
from src.repositories.emisor_repo import EmisorRepo
from db import get_db

from datetime import datetime

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

@comprobante.put("/comprobante/{id}", response_model=schemas.Comprobante)
def update_comprobante(
    id: int, comprobante: schemas.ComprobanteCreate, db: Session = Depends(get_db)
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

    return repo.ComprobanteRepo(db).update_comprobante(id, comprobante_data)


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


@comprobante.get("/comprobantes/sumar")
def get_comprobantes_sumar(
    cuit: int,
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    """
    Sumar los comprobantes filtrados por cuit, tipo de comprobante y fechas
    Si son Factura los suma si son Notas de credito lo resta
    """
    emisor = EmisorRepo(db).get_emisor_by_cuit(cuit)
    if not emisor:
        raise HTTPException(status_code=404, detail="Emisor no encontrado")
    comprobantes = repo.ComprobanteRepo(db).get_comprobantes_by_emisor_and_fechas(
        emisor.id, fecha_inicio, fecha_fin
    )
    tipos_comprobante = TipoComprobanteRepo(db).get_tipos_comprobantes()
    if not tipos_comprobante:
        raise HTTPException(status_code=404, detail="Tipo de comprobante no encontrado")
    id_factura = 0
    id_nota_credito = 0
    for tipo in tipos_comprobante:
        if tipo.nombre == "Factura":
            id_factura = tipo.id
        if tipo.nombre == "Nota de Crédito":
            id_nota_credito = tipo.id
    if not id_factura or not id_nota_credito:
        raise HTTPException(status_code=404, detail="Tipo de comprobante no encontrado")

    neto_gravado = 0
    neto_no_gravado = 0
    exento = 0
    otros_tributos = 0
    iva = 0
    total = 0

    for comprobante in comprobantes:
        signo = 1 if comprobante.tipo_comprobante_id == id_factura else -1 if comprobante.tipo_comprobante_id == id_nota_credito else 0
        if signo == 0:
            continue
        neto_gravado += signo * (comprobante.neto_gravado or 0)
        neto_no_gravado += signo * (comprobante.neto_no_gravado or 0)
        exento += signo * (comprobante.exento or 0)
        otros_tributos += signo * (comprobante.otros_tributos or 0)
        iva += signo * (comprobante.iva or 0)
        total += signo * (comprobante.total or 0)

    return {
        "cuit": cuit,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "neto_gravado": neto_gravado,
        "neto_no_gravado": neto_no_gravado,
        "exento": exento,
        "otros_tributos": otros_tributos,
        "iva": iva,
        "total": total,
    }


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
        archivo_comprobante = ArchivoComprobanteCreate(
            nombre_archivo=file.filename,
        )
        create_archivo_comprobante(archivo_comprobante, db)
    except Exception as e:
        pass
        # raise HTTPException(500, detail=f"Ya se cargo el archivo: {str(file.filename)}")
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
                # Determinar si es nota de crédito para hacer los importes negativos
                es_nota_credito = row["Tipo de Comprobante"] == "Nota de Crédito"
                multiplicador = -1 if es_nota_credito else 1
                
                comprobante_data = schemas.ComprobanteCreate(
                    fecha_emision=row["Fecha de Emisión"],
                    punto_venta=int(row["Punto de Venta"]),
                    numero_desde=int(row["Número Desde"]),
                    numero_hasta=int(row["Número Hasta"]),
                    cod_autorizacion=int(row["Cód. Autorización"]),
                    tipo_cambio=float(row["Tipo Cambio"]),
                    moneda=row["Moneda"],
                    neto_gravado=float(row["Imp. Neto Gravado"]) * multiplicador,
                    neto_no_gravado=float(row["Imp. Neto No Gravado"]) * multiplicador,
                    exento=float(row["Imp. Op. Exentas"]) * multiplicador,
                    otros_tributos=float(row["Otros Tributos"]) * multiplicador,
                    iva=float(row["IVA"]) * multiplicador,
                    total=float(row["Imp. Total"]) * multiplicador,
                    emisor=schemas.EmisorCreate(
                        cuit=row["Nro. Doc. Emisor"],
                        denominacion=row["Denominación Emisor"],
                        tipo_doc=str(row["Tipo Doc. Emisor"]),
                    ),
                    tipo_comprobante=schemas.TipoComprobanteCreate(
                        tipo_comprobante=1 if row["Tipo de Comprobante"] == "Factura" else (3 if row["Tipo de Comprobante"] == "Nota de Crédito" else int(row["Tipo de Comprobante"])),
                        nombre=f"Tipo-{1 if row['Tipo de Comprobante'] == 'Factura' else (3 if row['Tipo de Comprobante'] == 'Nota de Crédito' else int(row['Tipo de Comprobante']))}", # Si no existe igual no lo crea
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

@comprobante.get("/comprobantes/download")
async def download_comprobantes(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    """
    Descarga los comprobantes filtrados por fechas en formato CSV.
    """
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_inicio_fmt = fecha_inicio_dt.strftime("%d/%m/%Y")
        fecha_fin_fmt = fecha_fin_dt.strftime("%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    comprobantes = repo.ComprobanteRepo(db).get_comprobantes_by_fechas(
        fecha_inicio_fmt, fecha_fin_fmt
    )

    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes")
    
    tipos_comprobante = TipoComprobanteRepo(db).get_tipos_comprobantes()
    emisores = EmisorRepo(db).get_emisores()

    data = []
    for comprobante in comprobantes:
        tipo_comprobante = next(
            (t for t in tipos_comprobante if t.id == comprobante.tipo_comprobante_id), None
        )
        emisor = next(
            (e for e in emisores if e.id == comprobante.emisor_id), None
        )
        signo = -1 if tipo_comprobante and tipo_comprobante.nombre == "Nota de Crédito" else 1
        
        # Formatear fecha a DD/MM/YYYY
        fecha_formateada = comprobante.fecha_emision
        try:
            # Intentar parsear desde formato YYYY-MM-DD
            fecha_dt = datetime.strptime(comprobante.fecha_emision, "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d/%m/%Y")
        except ValueError:
            # Si ya está en formato DD/MM/YYYY, mantenerlo
            try:
                datetime.strptime(comprobante.fecha_emision, "%d/%m/%Y")
                fecha_formateada = comprobante.fecha_emision
            except ValueError:
                # Si no es ninguno de los formatos esperados, usar tal como está
                pass
        
        data.append({
            "Fecha de Emisión": fecha_formateada,
            "Tipo de Comprobante": tipo_comprobante.nombre if tipo_comprobante else "",
            "Punto de Venta": comprobante.punto_venta,
            "Número Desde": comprobante.numero_desde,
            "Número Hasta": comprobante.numero_hasta,
            "Cód. Autorización": comprobante.cod_autorizacion,
            "Tipo Doc. Emisor": emisor.tipo_doc if emisor else "",
            "Nro. Doc. Emisor": emisor.cuit if emisor else "",
            "Denominación Emisor": emisor.denominacion if emisor else "",
            "Tipo Cambio": comprobante.tipo_cambio,
            "Moneda": comprobante.moneda,
            "Imp. Neto Gravado": signo * (comprobante.neto_gravado or 0),
            "Imp. Neto No Gravado": signo * (comprobante.neto_no_gravado or 0),
            "Imp. Op. Exentas": signo * (comprobante.exento or 0),
            "IVA": signo * (comprobante.iva or 0),
            "Otros Tributos": signo * (comprobante.otros_tributos or 0),
            "Imp. Total": signo * (comprobante.total or 0),
        })

    csv_buffer = StringIO()
    df = pd.DataFrame(data)
    df.to_csv(csv_buffer, index=False, sep=';', decimal=',', quotechar='"')
    csv_buffer.seek(0)

    filename = f"comprobantes_{fecha_inicio}_a_{fecha_fin}.csv"
    
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@comprobante.get("/comprobantes/cuenta_corriente")
def get_comprobantes_cuenta_corriente(
    db: Session = Depends(get_db)
):
    """
    Obtiene los comprobantes que tienen cuenta corriente habilitada.
    """
    return repo.ComprobanteRepo(db).get_comprobantes_by_cuenta_corriente()

@comprobante.put("/comprobante/{id}/marcar_pagado", response_model=schemas.Comprobante)
def marcar_comprobante_como_pagado(
    id: int, 
    pago_data: schemas.ComprobantePago, 
    db: Session = Depends(get_db)
):
    """
    Marca un comprobante como pagado con fecha y número de ticket
    """
    return repo.ComprobanteRepo(db).marcar_como_pagado(
        id, pago_data.fecha_pago, pago_data.numero_ticket
    )

@comprobante.get("/comprobantes/cuenta_corriente/download")
async def download_comprobantes_cuenta_corriente(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    """
    Descarga los comprobantes de cuenta corriente filtrados por fechas en formato CSV.
    """
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_inicio_fmt = fecha_inicio_dt.strftime("%d/%m/%Y")
        fecha_fin_fmt = fecha_fin_dt.strftime("%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    comprobantes = repo.ComprobanteRepo(db).get_comprobantes_by_cuenta_corriente_and_fechas(
        fecha_inicio_fmt, fecha_fin_fmt
    )

    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes de cuenta corriente")
    
    tipos_comprobante = TipoComprobanteRepo(db).get_tipos_comprobantes()
    emisores = EmisorRepo(db).get_emisores()

    data = []
    for comprobante in comprobantes:
        tipo_comprobante = next(
            (t for t in tipos_comprobante if t.id == comprobante.tipo_comprobante_id), None
        )
        emisor = next(
            (e for e in emisores if e.id == comprobante.emisor_id), None
        )
        signo = -1 if tipo_comprobante and tipo_comprobante.nombre == "Nota de Crédito" else 1
        
        # Formatear fecha a DD/MM/YYYY
        fecha_formateada = comprobante.fecha_emision
        try:
            # Intentar parsear desde formato YYYY-MM-DD
            fecha_dt = datetime.strptime(comprobante.fecha_emision, "%Y-%m-%d")
            fecha_formateada = fecha_dt.strftime("%d/%m/%Y")
        except ValueError:
            # Si ya está en formato DD/MM/YYYY, mantenerlo
            try:
                datetime.strptime(comprobante.fecha_emision, "%d/%m/%Y")
                fecha_formateada = comprobante.fecha_emision
            except ValueError:
                # Si no es ninguno de los formatos esperados, usar tal como está
                pass
        
        data.append({
            "Fecha de Emisión": fecha_formateada,
            "Tipo de Comprobante": tipo_comprobante.nombre if tipo_comprobante else "",
            "Punto de Venta": comprobante.punto_venta,
            "Número Desde": comprobante.numero_desde,
            "Número Hasta": comprobante.numero_hasta,
            "Cód. Autorización": comprobante.cod_autorizacion,
            "Tipo Doc. Emisor": emisor.tipo_doc if emisor else "",
            "Nro. Doc. Emisor": emisor.cuit if emisor else "",
            "Denominación Emisor": emisor.denominacion if emisor else "",
            "Tipo Cambio": comprobante.tipo_cambio,
            "Moneda": comprobante.moneda,
            "Imp. Neto Gravado": signo * (comprobante.neto_gravado or 0),
            "Imp. Neto No Gravado": signo * (comprobante.neto_no_gravado or 0),
            "Imp. Op. Exentas": signo * (comprobante.exento or 0),
            "IVA": signo * (comprobante.iva or 0),
            "Otros Tributos": signo * (comprobante.otros_tributos or 0),
            "Imp. Total": signo * (comprobante.total or 0),
            "Fecha Pago": comprobante.fecha_pago or "",
            "Número Ticket": comprobante.numero_ticket or "",
        })

    csv_buffer = StringIO()
    df = pd.DataFrame(data)
    df.to_csv(csv_buffer, index=False, sep=';', decimal=',', quotechar='"')
    csv_buffer.seek(0)

    filename = f"cuenta_corriente_{fecha_inicio}_a_{fecha_fin}.csv"
    
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

