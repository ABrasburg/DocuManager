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


def test_sumar_descuenta_nota_credito(client, farmacia_params, emisor_payload):
    client.post("/tipo_comprobante", params=farmacia_params, json={"tipo_comprobante": 1, "nombre": "Factura"})
    client.post("/tipo_comprobante", params=farmacia_params, json={"tipo_comprobante": 3, "nombre": "Nota de Crédito"})

    base = {
        "fecha_emision": "2026-04-01",
        "punto_venta": 1,
        "cod_autorizacion": 0,
        "tipo_cambio": 1.0,
        "moneda": "ARS",
        "neto_gravado": 0.0,
        "neto_no_gravado": 0.0,
        "otros_tributos": 0.0,
        "emisor": emisor_payload,
    }

    # Factura: total=121, iva=21, exento=0
    client.post("/comprobante", params=farmacia_params, json={
        **base,
        "numero_desde": 1, "numero_hasta": 1,
        "exento": 0.0, "iva": 21.0, "total": 121.0,
        "tipo_comprobante": {"tipo_comprobante": 1, "nombre": "Factura"},
    })

    # Nota de crédito ingresada manualmente con valores positivos
    client.post("/comprobante", params=farmacia_params, json={
        **base,
        "numero_desde": 2, "numero_hasta": 2,
        "exento": 0.0, "iva": 10.5, "total": 60.5,
        "tipo_comprobante": {"tipo_comprobante": 3, "nombre": "Nota de Crédito"},
    })

    response = client.get(
        "/comprobantes/sumar",
        params={**farmacia_params, "cuit": emisor_payload["cuit"], "fecha_inicio": "2026-04-01", "fecha_fin": "2026-04-30"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["iva"] == round(21.0 - 10.5, 2)
    assert data["total"] == round(121.0 - 60.5, 2)


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
