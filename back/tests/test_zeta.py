def test_zeta_crud_y_busqueda_por_fecha(client, farmacia_params, zeta_payload):
    response = client.get("/zetas", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/zeta", params=farmacia_params, json=zeta_payload)
    assert response.status_code == 200
    created = response.json()
    assert created["numero"] == 1
    assert created["punto_de_venta"] == 1
    assert created["iva"] == 121.0

    response = client.get(f"/zeta/{created['id']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

    response = client.get(
        "/zetas/fecha",
        params={**farmacia_params, "fecha_desde": "2026-04-01", "fecha_hasta": "2026-04-30"},
    )
    assert response.status_code == 200
    assert [z["id"] for z in response.json()] == [created["id"]]

    response = client.get(
        "/zetas/fecha",
        params={**farmacia_params, "fecha_desde": "01/04/2026", "fecha_hasta": "30/04/2026"},
    )
    assert response.status_code == 200
    assert [z["id"] for z in response.json()] == [created["id"]]

    response = client.get(
        "/zetas/download",
        params={**farmacia_params, "fecha_inicio": "2026-04-01", "fecha_fin": "2026-04-30"},
    )
    assert response.status_code == 200
    assert "Fecha" in response.text
    assert "300,0" in response.text

    response = client.delete(f"/zeta/{created['id']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
