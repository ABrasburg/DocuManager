import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


BACK_DIR = Path(__file__).resolve().parents[1]
TEST_DB = BACK_DIR / "test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}?check_same_thread=False&mode=rwc"
os.environ["ENVIRONMENT"] = "test"

from db import Base, engine
from main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def farmacia(client):
    response = client.post("/farmacia", json={"nombre": "Farmacia Test"})
    assert response.status_code == 201
    return response.json()


@pytest.fixture()
def farmacia_id(farmacia):
    return farmacia["id"]


@pytest.fixture()
def farmacia_params(farmacia_id):
    return {"farmacia_id": farmacia_id}


@pytest.fixture()
def tipo_payload():
    return {"tipo_comprobante": 1, "nombre": "Factura"}


@pytest.fixture()
def emisor_payload():
    return {
        "cuit": 20123456789,
        "tipo_doc": "CUIT",
        "denominacion": "Proveedor Test",
        "cuenta_corriente": False,
    }


@pytest.fixture()
def comprobante_payload(emisor_payload, tipo_payload):
    return {
        "fecha_emision": "2026-04-01",
        "punto_venta": 1,
        "numero_desde": 1,
        "numero_hasta": 1,
        "cod_autorizacion": 12323,
        "tipo_cambio": 1.0,
        "moneda": "ARS",
        "neto_gravado": 100.0,
        "neto_no_gravado": 5.0,
        "exento": 10.0,
        "otros_tributos": 2.0,
        "iva": 121.0,
        "total": 238.0,
        "emisor": emisor_payload,
        "tipo_comprobante": tipo_payload,
    }


@pytest.fixture()
def zeta_payload():
    return {
        "fecha": "2026-04-01T00:00:00",
        "punto_de_venta": 1,
        "numero": 1,
        "ultimo_ticket": 10,
        "exento": 20.0,
        "iva": 121.0,
        "perfumeria": 30.0,
        "medicamentos_iva": 40.0,
        "total": 300.0,
    }


@pytest.fixture()
def tipo_comprobante(client, farmacia_params, tipo_payload):
    response = client.post("/tipo_comprobante", params=farmacia_params, json=tipo_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture()
def comprobante(client, farmacia_params, tipo_comprobante, comprobante_payload):
    response = client.post("/comprobante", params=farmacia_params, json=comprobante_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture()
def zeta(client, farmacia_params, zeta_payload):
    response = client.post("/zeta", params=farmacia_params, json=zeta_payload)
    assert response.status_code == 200
    return response.json()
