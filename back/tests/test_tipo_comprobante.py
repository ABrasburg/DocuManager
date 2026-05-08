def test_tipo_comprobante_crud(client, farmacia_params, tipo_payload):
    response = client.get("/tipos_comprobantes", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/tipo_comprobante", params=farmacia_params, json=tipo_payload)
    assert response.status_code == 201
    created = response.json()
    assert created["tipo_comprobante"] == tipo_payload["tipo_comprobante"]
    assert created["nombre"] == tipo_payload["nombre"]

    response = client.get("/tipo_comprobante/1", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == created

    response = client.get("/tipos_comprobantes", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == [created]

    response = client.delete("/tipo_comprobante/1", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == created

    response = client.get("/tipos_comprobantes", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == []


def test_tipos_comprobante_estan_aislados_por_farmacia(client, tipo_payload):
    farmacia_a = client.post("/farmacia", json={"nombre": "Farmacia A"}).json()
    farmacia_b = client.post("/farmacia", json={"nombre": "Farmacia B"}).json()

    response_a = client.post(
        "/tipo_comprobante",
        params={"farmacia_id": farmacia_a["id"]},
        json=tipo_payload,
    )
    response_b = client.post(
        "/tipo_comprobante",
        params={"farmacia_id": farmacia_b["id"]},
        json={**tipo_payload, "nombre": "Factura B"},
    )

    assert response_a.status_code == 201
    assert response_b.status_code == 201

    response = client.get("/tipos_comprobantes", params={"farmacia_id": farmacia_a["id"]})
    assert response.status_code == 200
    assert response.json() == [response_a.json()]
