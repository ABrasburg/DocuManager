from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.getcwd())
print(sys.path)
from main import app
from db import Base, engine, SessionLocal
from dotenv import load_dotenv

from src.models.emisor import Emisor

load_dotenv()
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def setup_module():
    """Preparar la base de datos para las pruebas"""
    db = SessionLocal()
    try:
        # Limpiar tablas antes de las pruebas
        db.query(Emisor).delete()
        db.commit()
    finally:
        db.close()
setup_module()

def test_create_emisor():
    response = client.post(
        "/emisor",
        json={
            "cuit": 20333333333,
            "denominacion": "Test Emisor",
            "tipo_doc": "80"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["cuit"] == 20333333333
    assert data["denominacion"] == "Test Emisor"

def test_get_emisores():
    response = client.get("/emisores")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_emisor():
    response = client.get("/emisor/20333333333")
    assert response.status_code == 200
    data = response.json()
    assert data["cuit"] == 20333333333
    assert data["tipo_doc"] == "80"
    assert data["denominacion"] == "Test Emisor"

def test_delete_emisor():
    response = client.delete("/emisor/20333333333")
    assert response.status_code == 200
    data = response.json()
    assert data["cuit"] == 20333333333
    assert data["denominacion"] == "Test Emisor"
