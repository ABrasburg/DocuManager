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


def get_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return repo.ComprobanteRepo(db, farmacia_id)


def get_tipo_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return TipoComprobanteRepo(db, farmacia_id)


def get_emisor_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return EmisorRepo(db, farmacia_id)


def get_zeta_repo(farmacia_id: int, db: Session = Depends(get_db)):
    return ZetaRepo(db, farmacia_id)


@comprobante.get("/comprobantes", response_model=List[schemas.Comprobante])
def get_comprobantes(r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.get_comprobantes()


@comprobante.post("/comprobante", response_model=schemas.Comprobante, status_code=201)
def create_comprobante(
    comprobante: schemas.ComprobanteCreate,
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    db_tipo = tipo_repo.get_tipo_comprobante(comprobante.tipo_comprobante.tipo_comprobante)
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de comprobante no encontrado")

    db_emisor = emisor_repo.get_emisor(comprobante.emisor.cuit)
    if not db_emisor:
        db_emisor = emisor_repo.create_emisor(comprobante.emisor)

    comprobante_data = comprobante.model_dump()
    comprobante_data["emisor_id"] = db_emisor.id
    comprobante_data["tipo_comprobante_id"] = db_tipo.id
    comprobante_data.pop("emisor", None)
    comprobante_data.pop("tipo_comprobante", None)

    return r.create_comprobante(comprobante_data)


@comprobante.delete("/comprobante/{id}", response_model=schemas.Comprobante)
def delete_comprobante(id: int, r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.delete_comprobante(id)


@comprobante.put("/comprobante/{id}", response_model=schemas.Comprobante)
def update_comprobante(
    id: int,
    comprobante: schemas.ComprobanteCreate,
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    db_tipo = tipo_repo.get_tipo_comprobante(comprobante.tipo_comprobante.tipo_comprobante)
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de comprobante no encontrado")

    db_emisor = emisor_repo.get_emisor(comprobante.emisor.cuit)
    if not db_emisor:
        db_emisor = emisor_repo.create_emisor(comprobante.emisor)

    comprobante_data = comprobante.model_dump()
    comprobante_data["emisor_id"] = db_emisor.id
    comprobante_data["tipo_comprobante_id"] = db_tipo.id
    comprobante_data.pop("emisor", None)
    comprobante_data.pop("tipo_comprobante", None)

    return r.update_comprobante(id, comprobante_data)


@comprobante.get("/comprobante/{id}", response_model=schemas.Comprobante)
def get_comprobante(id: int, r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.get_comprobante(id)


@comprobante.get("/comprobantes/emisor/{cuit}", response_model=List[schemas.Comprobante])
def get_comprobantes_by_emisor(cuit: int, r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.get_comprobantes_by_emisor(cuit)


@comprobante.get("/comprobantes/fechas", response_model=List[schemas.Comprobante])
def get_comprobantes_by_fechas(fecha_inicio: str, fecha_fin: str, r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.get_comprobantes_by_fechas(fecha_inicio, fecha_fin)


@comprobante.get("/comprobantes/sumar")
def get_comprobantes_sumar(
    cuit: int,
    fecha_inicio: str,
    fecha_fin: str,
    r: repo.ComprobanteRepo = Depends(get_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    emisor = emisor_repo.get_emisor(cuit)
    if not emisor:
        raise HTTPException(status_code=404, detail="Emisor no encontrado")
    comprobantes = r.get_comprobantes_by_emisor(emisor.id)

    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
    fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")

    exento = otros_tributos = iva = total = 0
    for c in comprobantes:
        try:
            try:
                fecha_c = datetime.strptime(c.fecha_emision, "%Y-%m-%d")
            except ValueError:
                fecha_c = datetime.strptime(c.fecha_emision, "%d/%m/%Y")
            if fecha_inicio_dt <= fecha_c <= fecha_fin_dt:
                exento += (c.exento or 0) + (c.neto_no_gravado or 0)
                otros_tributos += c.otros_tributos or 0
                iva += c.iva or 0
                total += c.total or 0
        except Exception:
            continue

    gravado = iva / 1.21 if iva else 0

    return {
        "cuit": cuit,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "gravado": round(gravado, 2),
        "exento": round(exento, 2),
        "otros_tributos": round(otros_tributos, 2),
        "iva": round(iva, 2),
        "total": round(total, 2),
    }


@comprobante.post("/comprobantes/upload")
async def upload_comprobantes(
    file: UploadFile = File(...),
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
    db: Session = Depends(get_db),
    farmacia_id: int = 0,
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, detail="Solo se permiten archivos CSV")
    try:
        contents = await file.read()
        content_str = contents.decode('utf-8-sig')

        csv_reader = csv.DictReader(StringIO(content_str), delimiter=';', quotechar='"')
        rows = list(csv_reader)
        if not rows:
            raise HTTPException(400, detail="El archivo CSV está vacío")

        columns = set(rows[0].keys())
        base_required_columns = {
            "Fecha de Emisión", "Tipo de Comprobante", "Punto de Venta",
            "Número Desde", "Número Hasta", "Cód. Autorización",
            "Tipo Doc. Emisor", "Nro. Doc. Emisor", "Denominación Emisor",
            "Tipo Cambio", "Moneda", "Imp. Neto No Gravado",
            "Imp. Op. Exentas", "Otros Tributos", "Imp. Total",
        }

        has_new_format = "Imp. Neto Gravado Total" in columns and "Total IVA" in columns
        has_old_format = "Imp. Neto Gravado" in columns and "IVA" in columns

        if has_new_format:
            required_columns = base_required_columns | {"Imp. Neto Gravado Total", "Total IVA"}
        elif has_old_format:
            required_columns = base_required_columns | {"Imp. Neto Gravado", "IVA"}
        else:
            raise HTTPException(status_code=400, detail="Formato de CSV no reconocido")

        if not required_columns.issubset(columns):
            missing = required_columns - columns
            raise HTTPException(status_code=400, detail=f"Faltan columnas: {missing}")

        def safe_int_early(value, default=0):
            if not value or value == '':
                return default
            try:
                return int(str(value).replace('-', '').replace('/', '').replace(' ', '').strip() or str(default))
            except (ValueError, TypeError):
                return default

        max_numero_hasta = max(safe_int_early(row["Número Hasta"]) for row in rows if row.get("Número Hasta"))

        resultados = []

        for index, row in enumerate(rows):
            try:
                neto_gravado_field = "Imp. Neto Gravado Total" if has_new_format else "Imp. Neto Gravado"
                iva_field = "Total IVA" if has_new_format else "IVA"
                numeric_fields = ["Tipo Cambio", neto_gravado_field, "Imp. Neto No Gravado", "Imp. Op. Exentas", "Otros Tributos", iva_field, "Imp. Total"]

                def safe_float(value, default=0.0):
                    if not value or value == '':
                        return default
                    try:
                        return float(str(value).replace(',', '.'))
                    except (ValueError, TypeError):
                        return default

                def safe_int(value, default=0):
                    if not value or value == '':
                        return default
                    try:
                        return int(str(value).replace('-', '').replace('/', '').replace(' ', '').strip() or str(default))
                    except (ValueError, TypeError):
                        return default

                def normalize_date(date_str):
                    if not date_str or date_str == '':
                        return None
                    date_str = str(date_str).strip()
                    if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            return date_str
                        except ValueError:
                            pass
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d']:
                        try:
                            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                    return date_str

                for field in numeric_fields:
                    if field in row and row[field]:
                        row[field] = row[field].replace(',', '.')

                punto_venta = safe_int(row["Punto de Venta"])
                numero_desde = safe_int(row["Número Desde"])
                numero_hasta = safe_int(row["Número Hasta"])

                if r.exists_comprobante_by_numero(punto_venta, numero_desde, numero_hasta):
                    resultados.append({"fila": index + 1, "estado": "error", "error": f"El comprobante número {numero_desde} ya existe."})
                    continue

                es_nota_credito = row["Tipo de Comprobante"] in ("Nota de Crédito", "3")
                multiplicador = -1 if es_nota_credito else 1

                def tipo_num(t):
                    if t in ("1", "Factura"):
                        return 1
                    if t in ("2", "Nota de Débito"):
                        return 2
                    if t in ("3", "Nota de Crédito"):
                        return 3
                    return safe_int(t, 1)

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
                        tipo_comprobante=tipo_num(row["Tipo de Comprobante"]),
                        nombre=f"Tipo-{tipo_num(row['Tipo de Comprobante'])}",
                    ),
                )

                create_comprobante(comprobante_data, r, tipo_repo, emisor_repo)
                resultados.append({"fila": index + 1, "estado": "éxito", "error": None})

            except HTTPException as e:
                resultados.append({"fila": index + 1, "estado": "error", "error": e.detail})
            except Exception as e:
                resultados.append({"fila": index + 1, "estado": "error", "error": str(e)})

        exitos = sum(1 for r in resultados if r["estado"] == "éxito")
        errores = len(resultados) - exitos

        if exitos > 0:
            try:
                create_archivo_comprobante(
                    ArchivoComprobanteCreate(nombre_archivo=file.filename, numero_hasta=max_numero_hasta),
                    db
                )
            except Exception:
                pass

        return {"mensaje": f"Procesado completo. Éxitos: {exitos}, Errores: {errores}", "detalles": resultados}

    except csv.Error:
        raise HTTPException(400, detail="El archivo CSV no tiene un formato válido")
    except Exception as e:
        raise HTTPException(500, detail=f"Error al procesar el archivo: {str(e)}")


def _format_fecha(fecha_emision: str) -> str:
    try:
        return datetime.strptime(fecha_emision, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return fecha_emision


def _comprobantes_to_csv(comprobantes, tipos_comprobante, emisores, extra_fields=None):
    data = []
    for c in comprobantes:
        tipo = next((t for t in tipos_comprobante if t.id == c.tipo_comprobante_id), None)
        emisor = next((e for e in emisores if e.id == c.emisor_id), None)
        row = {
            "Fecha de Emisión": _format_fecha(c.fecha_emision),
            "Tipo de Comprobante": tipo.nombre if tipo else "",
            "Punto de Venta": c.punto_venta,
            "Número Desde": c.numero_desde,
            "Número Hasta": c.numero_hasta,
            "Cód. Autorización": c.cod_autorizacion,
            "Tipo Doc. Emisor": emisor.tipo_doc if emisor else "",
            "Nro. Doc. Emisor": emisor.cuit if emisor else "",
            "Denominación Emisor": emisor.denominacion if emisor else "",
            "Tipo Cambio": c.tipo_cambio,
            "Moneda": c.moneda,
            "Imp. Neto Gravado": c.neto_gravado or 0,
            "Imp. Neto No Gravado": c.neto_no_gravado or 0,
            "Imp. Op. Exentas": c.exento or 0,
            "IVA": c.iva or 0,
            "Otros Tributos": c.otros_tributos or 0,
            "Imp. Total": c.total or 0,
        }
        if extra_fields:
            row.update(extra_fields(c))
        data.append(row)
    return data


def _to_streaming_csv(data, filename):
    csv_buffer = StringIO()
    if data:
        writer = csv.DictWriter(csv_buffer, fieldnames=data[0].keys(), delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in data:
            writer.writerow({k: str(v).replace('.', ',') if isinstance(v, float) else v for k, v in row.items()})
    csv_buffer.seek(0)
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@comprobante.get("/comprobantes/download")
async def download_comprobantes(
    fecha_inicio: str,
    fecha_fin: str,
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    try:
        fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
        ff = datetime.strptime(fecha_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    comprobantes = r.get_comprobantes_by_fechas(fi, ff)
    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes")

    data = _comprobantes_to_csv(comprobantes, tipo_repo.get_tipos_comprobantes(), emisor_repo.get_emisores())
    return _to_streaming_csv(data, f"comprobantes_{fecha_inicio}_a_{fecha_fin}.csv")


@comprobante.get("/comprobantes/cuenta_corriente")
def get_comprobantes_cuenta_corriente(r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.get_comprobantes_by_cuenta_corriente()


@comprobante.put("/comprobante/{id}/marcar_pagado", response_model=schemas.Comprobante)
def marcar_comprobante_como_pagado(id: int, pago_data: schemas.ComprobantePago, r: repo.ComprobanteRepo = Depends(get_repo)):
    return r.marcar_como_pagado(id, pago_data.fecha_pago, pago_data.numero_ticket)


@comprobante.get("/comprobantes/cuenta_corriente/download")
async def download_comprobantes_cuenta_corriente(
    fecha_inicio: str,
    fecha_fin: str,
    emisor_cuit: str = None,
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    try:
        fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
        ff = datetime.strptime(fecha_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    comprobantes = r.get_comprobantes_by_cuenta_corriente_and_fechas(fi, ff, emisor_cuit)
    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes de cuenta corriente")

    data = _comprobantes_to_csv(
        comprobantes,
        tipo_repo.get_tipos_comprobantes(),
        emisor_repo.get_emisores(),
        extra_fields=lambda c: {"Fecha Pago": c.fecha_pago or "", "Número Ticket": c.numero_ticket or ""}
    )
    return _to_streaming_csv(data, f"cuenta_corriente_{fecha_inicio}_a_{fecha_fin}.csv")


@comprobante.get("/comprobantes/cuenta_corriente/impagos/download")
async def download_comprobantes_impagos(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    emisor_cuit: str = None,
    r: repo.ComprobanteRepo = Depends(get_repo),
    tipo_repo: TipoComprobanteRepo = Depends(get_tipo_repo),
    emisor_repo: EmisorRepo = Depends(get_emisor_repo),
):
    fi_fmt = ff_fmt = None
    if fecha_inicio and fecha_fin:
        try:
            fi_fmt = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
            ff_fmt = datetime.strptime(fecha_fin, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    comprobantes = r.get_comprobantes_impagos_cuenta_corriente(fi_fmt, ff_fmt, emisor_cuit)
    if not comprobantes:
        raise HTTPException(status_code=404, detail="No se encontraron comprobantes impagos")

    data = _comprobantes_to_csv(comprobantes, tipo_repo.get_tipos_comprobantes(), emisor_repo.get_emisores())
    filename = f"comprobantes_impagos_{fecha_inicio}_a_{fecha_fin}.csv" if fecha_inicio else f"comprobantes_impagos_{datetime.now().strftime('%Y%m%d')}.csv"
    return _to_streaming_csv(data, filename)


@comprobante.get("/comprobantes/reporte_afip")
async def generar_reporte_afip(
    fecha_inicio: str,
    fecha_fin: str,
    r: repo.ComprobanteRepo = Depends(get_repo),
    zeta_r: ZetaRepo = Depends(get_zeta_repo),
):
    try:
        fi_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        ff_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fi_fmt = fi_dt.strftime("%d/%m/%Y")
        ff_fmt = ff_dt.strftime("%d/%m/%Y")
        cantidad_dias = (ff_dt - fi_dt).days + 1
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    zetas = zeta_r.get_zetas_by_fecha(fi_fmt, ff_fmt)
    exento = sum(z.exento or 0 for z in zetas)
    perfumeria = sum(z.perfumeria or 0 for z in zetas)
    medicamentos_iva = sum(z.medicamentos_iva or 0 for z in zetas)
    iva = sum(z.iva or 0 for z in zetas)
    total = sum(z.total or 0 for z in zetas)
    gravado = iva / 1.21 if iva else 0

    return {
        "periodo": {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "cantidad_dias": cantidad_dias},
        "exento": round(exento, 2),
        "gravado": round(gravado, 2),
        "perfumeria": round(perfumeria, 2),
        "medicamentos_iva": round(medicamentos_iva, 2),
        "iva": round(iva, 2),
        "total": round(total, 2),
    }
