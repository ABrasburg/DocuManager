from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from sqlalchemy.orm import Session
import src.schemas.comprobante_schema as schemas
import src.repositories.comprobante_repo as repo
from src.repositories.tipo_comprobante_repo import TipoComprobanteRepo
from src.routes.archivo_comprobante import create_archivo_comprobante
from src.schemas.archivo_comprobante_schema import ArchivoComprobanteCreate
from src.repositories.emisor_repo import EmisorRepo
from src.repositories.zeta_repo import ZetaRepo
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
    Sumar los comprobantes filtrados por cuit y fechas.
    Las notas de crédito ya se almacenan con valores negativos en la BD,
    por lo que solo se necesita sumar todos los valores directamente.
    """
    emisor = EmisorRepo(db).get_emisor_by_cuit(cuit)
    if not emisor:
        raise HTTPException(status_code=404, detail="Emisor no encontrado")
    comprobantes = repo.ComprobanteRepo(db).get_comprobantes_by_emisor_and_fechas(
        emisor.id, fecha_inicio, fecha_fin
    )

    neto_gravado = 0
    neto_no_gravado = 0
    exento = 0
    otros_tributos = 0
    iva = 0
    total = 0

    # Sumar directamente - las notas de crédito ya tienen valores negativos
    for comprobante in comprobantes:
        neto_gravado += (comprobante.neto_gravado or 0)
        neto_no_gravado += (comprobante.neto_no_gravado or 0)
        exento += (comprobante.exento or 0)
        otros_tributos += (comprobante.otros_tributos or 0)
        iva += (comprobante.iva or 0)
        total += (comprobante.total or 0)

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
        contents = await file.read()
        content_str = contents.decode('utf-8-sig')
        
        csv_reader = csv.DictReader(
            StringIO(content_str),
            delimiter=';',
            quotechar='"'
        )

        rows = list(csv_reader)
        if not rows:
            raise HTTPException(400, detail="El archivo CSV está vacío")

        # Detectar formato de CSV basado en las columnas disponibles
        columns = set(rows[0].keys())

        # Columnas base requeridas en ambos formatos
        base_required_columns = {
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
            "Imp. Neto No Gravado",
            "Imp. Op. Exentas",
            "Otros Tributos",
            "Imp. Total",
        }

        # Determinar si es formato nuevo (AFIP detallado) o formato original
        has_new_format_columns = "Imp. Neto Gravado Total" in columns and "Total IVA" in columns
        has_original_format_columns = "Imp. Neto Gravado" in columns and "IVA" in columns

        if has_new_format_columns:
            # Formato nuevo AFIP
            required_columns = base_required_columns | {"Imp. Neto Gravado Total", "Total IVA"}
        elif has_original_format_columns:
            # Formato original
            required_columns = base_required_columns | {"Imp. Neto Gravado", "IVA"}
        else:
            raise HTTPException(
                status_code=400,
                detail="El archivo CSV no tiene el formato correcto. Debe contener columnas de IVA en formato original ('Imp. Neto Gravado' + 'IVA') o formato AFIP ('Imp. Neto Gravado Total' + 'Total IVA')",
            )

        if not required_columns.issubset(columns):
            missing = required_columns - columns
            raise HTTPException(
                status_code=400,
                detail=f"El archivo CSV no tiene las columnas requeridas. Faltan: {missing}",
            )

        # Función helper para safe_int (necesario antes del loop)
        def safe_int_early(value, default=0):
            """Convierte un valor a int, devolviendo default si está vacío o es None"""
            if not value or value == '' or value is None:
                return default
            try:
                # Limpiar separadores comunes (-, /, espacios) antes de convertir
                cleaned_value = str(value).replace('-', '').replace('/', '').replace(' ', '').strip()
                return int(cleaned_value) if cleaned_value else default
            except (ValueError, TypeError):
                return default

        max_numero_hasta = max(safe_int_early(row["Número Hasta"]) for row in rows if row.get("Número Hasta"))

        resultados = []
        comprobante_repo = repo.ComprobanteRepo(db)
        
        for index, row in enumerate(rows):
            try:
                # Mapear columnas según el formato detectado
                if has_new_format_columns:
                    # Formato nuevo AFIP - mapear a nombres esperados por el backend
                    neto_gravado_field = "Imp. Neto Gravado Total"
                    iva_field = "Total IVA"
                    numeric_fields = ["Tipo Cambio", "Imp. Neto Gravado Total", "Imp. Neto No Gravado", "Imp. Op. Exentas", "Otros Tributos", "Total IVA", "Imp. Total"]
                else:
                    # Formato original
                    neto_gravado_field = "Imp. Neto Gravado"
                    iva_field = "IVA"
                    numeric_fields = ["Tipo Cambio", "Imp. Neto Gravado", "Imp. Neto No Gravado", "Imp. Op. Exentas", "Otros Tributos", "IVA", "Imp. Total"]

                # Función helper para convertir campos numéricos con manejo de valores nulos
                def safe_float(value, default=0.0):
                    """Convierte un valor a float, devolviendo default si está vacío o es None"""
                    if not value or value == '' or value is None:
                        return default
                    try:
                        return float(str(value).replace(',', '.'))
                    except (ValueError, TypeError):
                        return default

                def safe_int(value, default=0):
                    """Convierte un valor a int, devolviendo default si está vacío o es None"""
                    if not value or value == '' or value is None:
                        return default
                    try:
                        # Limpiar separadores comunes (-, /, espacios) antes de convertir
                        cleaned_value = str(value).replace('-', '').replace('/', '').replace(' ', '').strip()
                        return int(cleaned_value) if cleaned_value else default
                    except (ValueError, TypeError):
                        return default

                def normalize_date(date_str):
                    """
                    Normaliza una fecha a formato ISO (YYYY-MM-DD).
                    Soporta formatos: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, YYYY/MM/DD
                    """
                    if not date_str or date_str == '':
                        return None

                    date_str = str(date_str).strip()

                    # Si ya está en formato ISO, retornar
                    if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            return date_str
                        except ValueError:
                            pass

                    # Intentar diferentes formatos
                    formats = [
                        '%d/%m/%Y',  # 22/10/2025
                        '%d-%m-%Y',  # 22-10-2025
                        '%Y/%m/%d',  # 2025/10/22
                        '%Y-%m-%d',  # 2025-10-22
                    ]

                    for fmt in formats:
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            return date_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            continue

                    # Si no se pudo parsear, retornar como está
                    return date_str

                # Reemplazar comas por puntos en campos numéricos
                for field in numeric_fields:
                    if field in row and row[field]:
                        row[field] = row[field].replace(',', '.')

                punto_venta = safe_int(row["Punto de Venta"])
                numero_desde = safe_int(row["Número Desde"])
                numero_hasta = safe_int(row["Número Hasta"])

                if comprobante_repo.exists_comprobante_by_numero(punto_venta, numero_desde, numero_hasta):
                    resultados.append({
                        "fila": index + 1,
                        "estado": "error",
                        "error": f"El comprobante número {numero_desde} ya se encuentra en el sistema."
                    })
                    continue

                es_nota_credito = row["Tipo de Comprobante"] == "Nota de Crédito" or row["Tipo de Comprobante"] == "3"
                multiplicador = -1 if es_nota_credito else 1

                comprobante_data = schemas.ComprobanteCreate(
                    fecha_emision=normalize_date(row["Fecha de Emisión"]),
                    punto_venta=punto_venta,
                    numero_desde=numero_desde,
                    numero_hasta=numero_hasta,
                    cod_autorizacion=safe_int(row["Cód. Autorización"]),
                    tipo_cambio=safe_float(row["Tipo Cambio"], 1.0),
                    moneda=row["Moneda"],
                    neto_gravado=safe_float(row[neto_gravado_field]) * multiplicador,
                    neto_no_gravado=safe_float(row["Imp. Neto No Gravado"]) * multiplicador,
                    exento=safe_float(row["Imp. Op. Exentas"]) * multiplicador,
                    otros_tributos=safe_float(row["Otros Tributos"]) * multiplicador,
                    iva=safe_float(row[iva_field]) * multiplicador,
                    total=safe_float(row["Imp. Total"]) * multiplicador,
                    emisor=schemas.EmisorCreate(
                        cuit=row["Nro. Doc. Emisor"],
                        denominacion=row["Denominación Emisor"],
                        tipo_doc=str(row["Tipo Doc. Emisor"]),
                    ),
                    tipo_comprobante=schemas.TipoComprobanteCreate(
                        tipo_comprobante=1 if row["Tipo de Comprobante"] == "1" or row["Tipo de Comprobante"] == "Factura" else (2 if row["Tipo de Comprobante"] == "2" or row["Tipo de Comprobante"] == "Nota de Débito" else (3 if row["Tipo de Comprobante"] == "3" or row["Tipo de Comprobante"] == "Nota de Crédito" else safe_int(row["Tipo de Comprobante"], 1))),
                        nombre=f"Tipo-{1 if row['Tipo de Comprobante'] == '1' or row['Tipo de Comprobante'] == 'Factura' else (2 if row['Tipo de Comprobante'] == '2' or row['Tipo de Comprobante'] == 'Nota de Débito' else (3 if row['Tipo de Comprobante'] == '3' or row['Tipo de Comprobante'] == 'Nota de Crédito' else safe_int(row['Tipo de Comprobante'], 1)))}", # Si no existe igual no lo crea
                    ),
                )

                response = create_comprobante(comprobante_data, db)
                resultados.append(
                    {"fila": index + 1, "estado": "éxito", "error": None}
                )

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
        
        if exitos > 0:
            try:
                archivo_comprobante = ArchivoComprobanteCreate(
                    nombre_archivo=file.filename,
                    numero_hasta=max_numero_hasta
                )
                create_archivo_comprobante(archivo_comprobante, db)
            except Exception as e:
                pass

        return {
            "mensaje": f"Procesado completo. Éxitos: {exitos}, Errores: {errores}",
            "detalles": resultados,
        }

    except csv.Error:
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
            "Imp. Neto Gravado": comprobante.neto_gravado or 0,
            "Imp. Neto No Gravado": comprobante.neto_no_gravado or 0,
            "Imp. Op. Exentas": comprobante.exento or 0,
            "IVA": comprobante.iva or 0,
            "Otros Tributos": comprobante.otros_tributos or 0,
            "Imp. Total": comprobante.total or 0,
        })

    csv_buffer = StringIO()
    if data:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in data:
            # Convertir números a formato con coma decimal
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (int, float)) and key.startswith('Imp.'):
                    formatted_row[key] = str(value).replace('.', ',')
                else:
                    formatted_row[key] = value
            writer.writerow(formatted_row)
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
            "Imp. Neto Gravado": comprobante.neto_gravado or 0,
            "Imp. Neto No Gravado": comprobante.neto_no_gravado or 0,
            "Imp. Op. Exentas": comprobante.exento or 0,
            "IVA": comprobante.iva or 0,
            "Otros Tributos": comprobante.otros_tributos or 0,
            "Imp. Total": comprobante.total or 0,
            "Fecha Pago": comprobante.fecha_pago or "",
            "Número Ticket": comprobante.numero_ticket or "",
        })

    csv_buffer = StringIO()
    if data:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in data:
            # Convertir números a formato con coma decimal
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (int, float)) and key.startswith('Imp.'):
                    formatted_row[key] = str(value).replace('.', ',')
                else:
                    formatted_row[key] = value
            writer.writerow(formatted_row)
    csv_buffer.seek(0)

    filename = f"cuenta_corriente_{fecha_inicio}_a_{fecha_fin}.csv"
    
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@comprobante.get("/comprobantes/cuenta_corriente/impagos/download")
async def download_comprobantes_impagos(
    db: Session = Depends(get_db),
):
    """
    Descarga todos los comprobantes impagos de cuenta corriente en formato CSV.
    """
    comprobantes = repo.ComprobanteRepo(db).get_comprobantes_impagos_cuenta_corriente()

    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes impagos")

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
            "Imp. Neto Gravado": comprobante.neto_gravado or 0,
            "Imp. Neto No Gravado": comprobante.neto_no_gravado or 0,
            "Imp. Op. Exentas": comprobante.exento or 0,
            "IVA": comprobante.iva or 0,
            "Otros Tributos": comprobante.otros_tributos or 0,
            "Imp. Total": comprobante.total or 0,
        })

    csv_buffer = StringIO()
    if data:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in data:
            # Convertir números a formato con coma decimal
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (int, float)) and key.startswith('Imp.'):
                    formatted_row[key] = str(value).replace('.', ',')
                else:
                    formatted_row[key] = value
            writer.writerow(formatted_row)
    csv_buffer.seek(0)

    filename = f"comprobantes_impagos_{datetime.now().strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@comprobante.get("/comprobantes/reporte_afip")
async def generar_reporte_afip(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
):
    """
    Genera un reporte estilo AFIP comparando Compras (Comprobantes) vs Ventas (Zetas)
    """
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_inicio_fmt = fecha_inicio_dt.strftime("%d/%m/%Y")
        fecha_fin_fmt = fecha_fin_dt.strftime("%d/%m/%Y")
        cantidad_dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    comprobante_repo = repo.ComprobanteRepo(db)
    zeta_repo = ZetaRepo(db)
    
    comprobantes = comprobante_repo.get_comprobantes_by_fechas(fecha_inicio_fmt, fecha_fin_fmt)
    compras_exento = sum(c.exento or 0 for c in comprobantes)
    compras_gravado = sum(c.neto_gravado or 0 for c in comprobantes)
    compras_iva = sum(c.iva or 0 for c in comprobantes)
    compras_subtotal = compras_exento + compras_gravado + compras_iva
    
    try:
        zetas = zeta_repo.get_zetas_by_fechas(fecha_inicio_fmt, fecha_fin_fmt)
    except AttributeError:
        zetas = zeta_repo.get_zetas()
        zetas_filtradas = []
        for z in zetas:
            try:
                fecha_z = z.fecha.strftime("%d/%m/%Y") if hasattr(z.fecha, 'strftime') else str(z.fecha)
                fecha_z_dt = datetime.strptime(fecha_z.split()[0], "%d/%m/%Y") if ' ' in str(fecha_z) else datetime.strptime(fecha_z, "%d/%m/%Y")
                if fecha_inicio_dt <= fecha_z_dt <= fecha_fin_dt:
                    zetas_filtradas.append(z)
            except:
                continue
        zetas = zetas_filtradas
    
    ventas_exento = sum(z.exento or 0 for z in zetas)
    ventas_perfumeria = sum(z.perfumeria or 0 for z in zetas)
    ventas_medicamentos_iva = sum(z.medicamentos_iva or 0 for z in zetas)
    ventas_iva = sum(z.iva or 0 for z in zetas)
    ventas_total = sum(z.total or 0 for z in zetas)

    # Total gravado de ventas = perfumería + medicamentos_iva
    ventas_gravado_total = ventas_perfumeria + ventas_medicamentos_iva

    diferencia_gravado = ventas_gravado_total - compras_gravado
    diferencia_total = ventas_total - compras_subtotal

    reporte = {
        "periodo": {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "cantidad_dias": cantidad_dias
        },
        "compras": {
            "subtotal_exento": round(compras_exento, 2),
            "subtotal_gravado": round(compras_gravado, 2),
            "iva": round(compras_iva, 2),
            "subtotal": round(compras_subtotal, 2)
        },
        "ventas": {
            "exento": round(ventas_exento, 2),
            "perfumeria": round(ventas_perfumeria, 2),
            "medicamentos_iva": round(ventas_medicamentos_iva, 2),
            "iva": round(ventas_iva, 2),
            "total": round(ventas_total, 2)
        },
        "diferencia": {
            "cantidad_dias": cantidad_dias,
            "gravado": round(diferencia_gravado, 2),
            "total": round(diferencia_total, 2)
        }
    }
    
    return reporte

