from sqlalchemy.orm import Session
from src.models.tipo_comprobante import TipoComprobante
from src.models.id_zeta import IdZeta


def init_db(db: Session):
    tipos_comprobantes = [(1, "Factura"), (3, "Nota de Crédito")]
    id_zetas  = [(8, 0), (9, 0)]

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
    
    # Crear los id_zeta
    for id_zeta in id_zetas:
        existing_id_zeta = db.query(IdZeta).filter_by(id=id_zeta[0]).first()
        if not existing_id_zeta:
            id_zeta_obj = IdZeta(id=id_zeta[0], contador=id_zeta[1])
            db.add(id_zeta_obj)

    # Confirmar todos los cambios
    db.commit()
