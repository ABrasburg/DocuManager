def test_farmacia_crud_basico(client):
    response = client.get("/farmacias")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/farmacia", json={"nombre": "Central"})
    assert response.status_code == 201
    created = response.json()
    assert created["id"] is not None
    assert created["nombre"] == "Central"

    response = client.get("/farmacias")
    assert response.status_code == 200
    assert response.json() == [created]
