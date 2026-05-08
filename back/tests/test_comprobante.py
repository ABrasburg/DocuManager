def test_comprobante_crud_y_consultas(
    client,
    farmacia_params,
    tipo_comprobante,
    comprobante_payload,
    emisor_payload,
):
    response = client.get("/comprobantes", params=farmacia_params)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/comprobante", params=farmacia_params, json=comprobante_payload)
    assert response.status_code == 201
    created = response.json()
    assert created["fecha_emision"] == "2026-04-01"
    assert created["emisor"]["cuit"] == emisor_payload["cuit"]
    assert created["tipo_comprobante"]["tipo_comprobante"] == 1

    response = client.get(f"/comprobante/{created['id']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

    response = client.get(
        f"/comprobantes/emisor/{emisor_payload['cuit']}",
        params=farmacia_params,
    )
    assert response.status_code == 200
    assert [c["id"] for c in response.json()] == [created["id"]]

    response = client.get(
        "/comprobantes/fechas",
        params={**farmacia_params, "fecha_inicio": "01/04/2026", "fecha_fin": "30/04/2026"},
    )
    assert response.status_code == 200
    assert [c["id"] for c in response.json()] == [created["id"]]

    response = client.get(
        "/comprobantes/sumar",
        params={
            **farmacia_params,
            "cuit": emisor_payload["cuit"],
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "cuit": emisor_payload["cuit"],
        "fecha_inicio": "2026-04-01",
        "fecha_fin": "2026-04-30",
        "gravado": 100.0,
        "exento": 15.0,
        "otros_tributos": 2.0,
        "iva": 121.0,
        "total": 238.0,
    }

    response = client.delete(f"/comprobante/{created['id']}", params=farmacia_params)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_comprobante_rechaza_tipo_inexistente(client, farmacia_params, comprobante_payload):
    response = client.post("/comprobante", params=farmacia_params, json=comprobante_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tipo de comprobante no encontrado"


def test_comprobante_download_csv(client, farmacia_params, comprobante):
    response = client.get(
        "/comprobantes/download",
        params={
            **farmacia_params,
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "comprobantes_2026-04-01_a_2026-04-30.csv" in response.headers["content-disposition"]
    assert "Fecha de Emisión" in response.text
    assert "Proveedor Test" in response.text


def test_cuenta_corriente_y_marcar_pagado(client, farmacia_params, comprobante, emisor_payload):
    response = client.put(
        f"/emisor/{emisor_payload['cuit']}/cuenta_corriente",
        params={**farmacia_params, "cuenta_corriente": True},
    )
    assert response.status_code == 200

    response = client.get("/comprobantes/cuenta_corriente", params=farmacia_params)
    assert response.status_code == 200
    assert [c["id"] for c in response.json()] == [comprobante["id"]]

    response = client.put(
        f"/comprobante/{comprobante['id']}/marcar_pagado",
        params=farmacia_params,
        json={"fecha_pago": "2026-04-15", "numero_ticket": "T-123"},
    )
    assert response.status_code == 200
    assert response.json()["fecha_pago"] == "2026-04-15"
    assert response.json()["numero_ticket"] == "T-123"

    response = client.get(
        "/comprobantes/cuenta_corriente/download",
        params={
            **farmacia_params,
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
        },
    )
    assert response.status_code == 200
    assert "Fecha Pago" in response.text
    assert "T-123" in response.text
