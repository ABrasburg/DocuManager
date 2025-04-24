from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.getcwd())
from main import app

from db import Base, engine, SessionLocal
from dotenv import load_dotenv
from aux_tests import setup_module

load_dotenv()
Base.metadata.create_all(bind=engine)

client = TestClient(app)

setup_module()

def test_get_zeta():
    response = client.get("/zetas")
    assert response.status_code == 200
    assert response.json() == []

test_zeta = {
        "fecha": "2023-01-01",
        "numero": 1,
        "ultimo_ticket": 1,
        "exento": 1,
        "iva": 1,
        "gravado": 1,
        "cuenta_corriente": "Test Cuenta Corriente",
        "total": 1
    }

def test_create_zeta():
    response = client.post("/zeta", json=test_zeta)
    assert response.status_code == 200
    assert response.json()["numero"] == 1
    assert response.json()["ultimo_ticket"] == 1
    assert response.json()["exento"] == 1
    assert response.json()["iva"] == 1
    assert response.json()["gravado"] == 1
    assert response.json()["cuenta_corriente"] == "Test Cuenta Corriente"
    assert response.json()["total"] == 1
    assert response.json()["id"] is not None

def test_get_zeta_con_zeta_existente():
    response = client.get("/zetas")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['numero'] == 1
    assert response.json()[0]['ultimo_ticket'] == 1
    assert response.json()[0]['exento'] == 1
    assert response.json()[0]['iva'] == 1

def test_get_zeta_by_id():
    response = client.get("/zeta/1")
    assert response.status_code == 200
    assert response.json()["numero"] == 1
    assert response.json()["ultimo_ticket"] == 1
    assert response.json()["exento"] == 1
    assert response.json()["iva"] == 1