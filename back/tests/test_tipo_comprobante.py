from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.getcwd())
print(sys.path)
from main import app

from db import Base, engine
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_get_tipos_comprobantes():
    response = client.get("/tipos_comprobantes")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "tipo_comprobante": 1, "nombre": "Factura"},
        {"id": 2, "tipo_comprobante": 3, "nombre": "Nota de Crédito"},
    ]


def test_create_tipo_comprobante():
    response = client.post(
        "/tipo_comprobante", json={"tipo_comprobante": 2, "nombre": "Nota de Débito"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "tipo_comprobante": 2,
        "nombre": "Nota de Débito",
    }


def test_get_tipos_comprobantes_con_nuevo():
    response = client.get("/tipos_comprobantes")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "tipo_comprobante": 1, "nombre": "Factura"},
        {"id": 2, "tipo_comprobante": 3, "nombre": "Nota de Crédito"},
        {"id": 3, "tipo_comprobante": 2, "nombre": "Nota de Débito"},
    ]


def test_delete_tipo_comprobante():
    response = client.delete("/tipo_comprobante/2")
    assert response.status_code == 200
    assert response.json() == {"id": 3, "tipo_comprobante": 2, "nombre": "Nota de Débito"}
