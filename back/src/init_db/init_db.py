from sqlalchemy.orm import Session
from src.models.tipo_comprobante import TipoComprobante


def init_db(db: Session):
    tipos_comprobantes = [(1, "Factura"), (3, "Nota de Crédito")]

    # Crear los tipos de comprobantes
    for tipo_comprobante in tipos_comprobantes:
        existing_tipo_comprobante = (
            db.query(TipoComprobante)
            .filter_by(tipo_comprobante=tipo_comprobante[0])
            .first()
        )
        if not existing_tipo_comprobante:
            tipo_comprobante_obj = TipoComprobante(
                tipo_comprobante=tipo_comprobante[0], nombre=tipo_comprobante[1]
            )
            db.add(tipo_comprobante_obj)

    # Confirmar todos los cambios
    db.commit()
