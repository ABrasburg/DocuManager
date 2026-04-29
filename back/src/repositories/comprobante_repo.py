from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from src.models.comprobante import Comprobante
from src.schemas.comprobante_schema import ComprobanteCreate


class ComprobanteRepo:
    def __init__(self, db: Session, farmacia_id: int):
        self.db = db
        self.farmacia_id = farmacia_id

    def _base_query(self):
        return self.db.query(Comprobante).filter(Comprobante.farmacia_id == self.farmacia_id)

    def get_comprobantes(self):
        return self._base_query().all()

    def get_comprobante(self, id: int):
        return self._base_query().filter(Comprobante.id == id).first()

    def create_comprobante(self, comprobante: dict):
        comprobante["farmacia_id"] = self.farmacia_id
        db_comprobante = Comprobante(**comprobante)
        self.db.add(db_comprobante)
        self.db.commit()
        self.db.refresh(db_comprobante)
        return db_comprobante

    def update_comprobante(self, id: int, comprobante: dict):
        db_comprobante = self._base_query().filter(Comprobante.id == id).first()
        if db_comprobante is None:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        for key, value in comprobante.items():
            setattr(db_comprobante, key, value)
        self.db.commit()
        self.db.refresh(db_comprobante)
        return db_comprobante

    def delete_comprobante(self, id: int):
        db_comprobante = self._base_query().filter(Comprobante.id == id).first()
        if db_comprobante is None:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        self.db.delete(db_comprobante)
        self.db.commit()
        return db_comprobante

    def get_comprobantes_by_fechas(self, fecha_inicio: str, fecha_fin: str):
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        resultado = []
        for c in self._base_query().all():
            try:
                try:
                    fecha_c = datetime.strptime(c.fecha_emision, "%Y-%m-%d")
                except ValueError:
                    fecha_c = datetime.strptime(c.fecha_emision, "%d/%m/%Y")
                if fecha_inicio_dt <= fecha_c <= fecha_fin_dt:
                    resultado.append(c)
            except Exception:
                continue
        return resultado

    def get_comprobantes_by_emisor(self, emisor_id: int):
        return self._base_query().filter(Comprobante.emisor_id == emisor_id).all()

    def get_comprobantes_by_cuenta_corriente(self):
        from src.models.emisor import Emisor
        return self._base_query().join(Emisor).filter(Emisor.cuenta_corriente == True).all()

    def get_comprobantes_by_cuenta_corriente_and_fechas(self, fecha_inicio: str, fecha_fin: str, emisor_cuit: str = None):
        from src.models.emisor import Emisor
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")

        query = self._base_query().join(Emisor).filter(Emisor.cuenta_corriente == True)
        if emisor_cuit:
            query = query.filter(Emisor.cuit == emisor_cuit)

        resultado = []
        for c in query.all():
            try:
                try:
                    fecha_c = datetime.strptime(c.fecha_emision, "%Y-%m-%d")
                except ValueError:
                    fecha_c = datetime.strptime(c.fecha_emision, "%d/%m/%Y")
                if fecha_inicio_dt <= fecha_c <= fecha_fin_dt:
                    resultado.append(c)
            except Exception:
                continue
        return resultado

    def get_comprobantes_impagos_cuenta_corriente(self, fecha_inicio: str = None, fecha_fin: str = None, emisor_cuit: str = None):
        from src.models.emisor import Emisor
        query = (
            self._base_query()
            .join(Emisor)
            .filter(Emisor.cuenta_corriente == True)
            .filter((Comprobante.fecha_pago == None) | (Comprobante.fecha_pago == ""))
        )
        if emisor_cuit:
            query = query.filter(Emisor.cuit == emisor_cuit)

        comprobantes = query.all()

        if not fecha_inicio or not fecha_fin:
            return comprobantes

        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        resultado = []
        for c in comprobantes:
            try:
                try:
                    fecha_c = datetime.strptime(c.fecha_emision, "%Y-%m-%d")
                except ValueError:
                    fecha_c = datetime.strptime(c.fecha_emision, "%d/%m/%Y")
                if fecha_inicio_dt <= fecha_c <= fecha_fin_dt:
                    resultado.append(c)
            except Exception:
                continue
        return resultado

    def marcar_como_pagado(self, id: int, fecha_pago: str, numero_ticket: str):
        db_comprobante = self._base_query().filter(Comprobante.id == id).first()
        if db_comprobante is None:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        db_comprobante.fecha_pago = fecha_pago
        db_comprobante.numero_ticket = numero_ticket
        self.db.commit()
        self.db.refresh(db_comprobante)
        return db_comprobante

    def exists_comprobante_by_numero(self, punto_venta: int, numero_desde: int, numero_hasta: int):
        return self._base_query().filter(
            Comprobante.punto_venta == punto_venta,
            Comprobante.numero_desde == numero_desde,
            Comprobante.numero_hasta == numero_hasta
        ).first() is not None
