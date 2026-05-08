def test_emisor_crud_y_cuenta_corriente(client, farmacia_params, emisor_payload):
    response = client.get("/emisores", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/emisor", params=farmacia_params, json=emisor_payload)
    assert response.status_code == 201
    created = response.json()
    assert created["cuit"] == emisor_payload["cuit"]
    assert created["denominacion"] == emisor_payload["denominacion"]
    assert created["cuenta_corriente"] is False

    response = client.get(f"/emisor/{emisor_payload['cuit']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == created

    updated_payload = {**emisor_payload, "denominacion": "Proveedor Actualizado"}
    response = client.put(
        f"/emisor/{emisor_payload['cuit']}",
        params=farmacia_params,
        json=updated_payload,
    )
    assert response.status_code == 200
    assert response.json()["denominacion"] == "Proveedor Actualizado"

    response = client.put(
        f"/emisor/{emisor_payload['cuit']}/cuenta_corriente",
        params={**farmacia_params, "cuenta_corriente": True},
    )
    assert response.status_code == 200
    assert response.json()["cuenta_corriente"] is True

    response = client.delete(f"/emisor/{emisor_payload['cuit']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json()["cuit"] == emisor_payload["cuit"]


def test_emisores_estan_aislados_por_farmacia(client, emisor_payload):
    farmacia_a = client.post("/farmacia", json={"nombre": "Farmacia A"}).json()
    farmacia_b = client.post("/farmacia", json={"nombre": "Farmacia B"}).json()

    response_a = client.post(
        "/emisor",
        params={"farmacia_id": farmacia_a["id"]},
        json=emisor_payload,
    )
    response_b = client.post(
        "/emisor",
        params={"farmacia_id": farmacia_b["id"]},
        json={**emisor_payload, "denominacion": "Proveedor B"},
    )

    assert response_a.status_code == 201
    assert response_b.status_code == 201

    response = client.get("/emisores", params={"farmacia_id": farmacia_a["id"]})
    assert response.status_code == 200
    assert response.json() == [response_a.json()]
