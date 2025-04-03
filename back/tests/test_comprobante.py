from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.getcwd())
print(sys.path)
from main import app

from db import Base, engine, SessionLocal
from dotenv import load_dotenv
from aux_tests import setup_module

load_dotenv()
Base.metadata.create_all(bind=engine)

client = TestClient(app)

setup_module()

def test_get_comprobantes():
    response = client.get("/comprobantes")
    assert response.status_code == 200
    assert response.json() == []

test_emisor = {
        "cuit": 20123456789,
        "tipo_doc": "CUIT",
        "denominacion": "Test Emisor"
    }
    
test_tipo = {
        "tipo_comprobante": 1,
        "nombre": "Factura"
    }
    
test_comprobante = {
        "fecha_emision": "2023-01-01",
        "punto_venta": 1,
        "numero_desde": 1,
        "numero_hasta": 1,
        "cod_autorizacion": 12323,
        "tipo_cambio": 1.0,
        "moneda": "ARS",
        "neto_gravado": 1000.0,
        "neto_no_gravado": 0.0,
        "exento": 0.0,
        "otros_tributos": 0.0,
        "iva": 210.0,
        "total": 1210.0,
        "emisor": test_emisor,
        "tipo_comprobante": test_tipo
    }

def test_create_comprobante():
    response = client.post("/comprobante", json=test_comprobante)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["fecha_emision"] == "2023-01-01"

def test_get_comprobantes_con_nuevo_tipo():
    nuevo_tipo = {
        "tipo_comprobante": 99,
        "nombre": "Nuevo tipo"
    }
    test_comprobante["tipo_comprobante"] = nuevo_tipo
    response = client.post("/comprobante", json=test_comprobante)
    assert response.status_code == 404

def test_borrar_comprobante():
    response = client.delete("/comprobante/1")
    assert response.status_code == 200
    assert response.json()["fecha_emision"] == "2023-01-01"