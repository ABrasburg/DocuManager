def test_reporte_afip_incluye_comprobantes_y_zetas_del_periodo(
    client,
    farmacia_params,
    comprobante,
    zeta,
):
    response = client.get(
        "/comprobantes/reporte_afip",
        params={
            **farmacia_params,
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "periodo": {
            "fecha_inicio": "2026-04-01",
            "fecha_fin": "2026-04-30",
            "cantidad_dias": 30,
        },
        "compras": {
            "subtotal_exento": 15.0,
            "subtotal_gravado": 100.0,
            "subtotal": 115.0,
        },
        "ventas": {
            "exento": 20.0,
            "gravado": 100.0,
            "perfumeria": 30.0,
            "medicamentos_iva": 40.0,
            "iva": 121.0,
            "total": 300.0,
        },
        "diferencia": {
            "cantidad_dias": 30,
            "gravado": 0.0,
            "total": 185.0,
        },
    }


def test_reporte_afip_descuenta_nota_credito_en_compras(client, farmacia_params, comprobante, zeta):
    # Crear tipo nota de crédito y emitir una manualmente (valores positivos en DB)
    client.post("/tipo_comprobante", params=farmacia_params, json={"tipo_comprobante": 3, "nombre": "Nota de Crédito"})
    client.post(
        "/comprobante",
        params=farmacia_params,
        json={
            "fecha_emision": "2026-04-15",
            "punto_venta": 1,
            "numero_desde": 99,
            "numero_hasta": 99,
            "cod_autorizacion": 0,
            "tipo_cambio": 1.0,
            "moneda": "ARS",
            "neto_gravado": 50.0,
            "neto_no_gravado": 0.0,
            "exento": 0.0,
            "otros_tributos": 0.0,
            "iva": 10.5,
            "total": 60.5,
            "emisor": {"cuit": 20123456789, "denominacion": "Prov NC", "tipo_doc": "CUIT"},
            "tipo_comprobante": {"tipo_comprobante": 3, "nombre": "Nota de Crédito"},
        },
    )

    response = client.get(
        "/comprobantes/reporte_afip",
        params={**farmacia_params, "fecha_inicio": "2026-04-01", "fecha_fin": "2026-04-30"},
    )
    assert response.status_code == 200
    data = response.json()
    # factura: gravado=100, exento=15 — nota crédito resta: gravado=50, exento=0
    assert data["compras"]["subtotal_gravado"] == round(100.0 - 50.0, 2)
    assert data["compras"]["subtotal_exento"] == round(15.0 - 0.0, 2)
    assert data["compras"]["subtotal"] == round(115.0 - 50.0, 2)


def test_reporte_afip_rechaza_fechas_invalidas(client, farmacia_params):
    response = client.get(
        "/comprobantes/reporte_afip",
        params={
            **farmacia_params,
            "fecha_inicio": "01/04/2026",
            "fecha_fin": "30/04/2026",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Formato de fecha inválido. Use YYYY-MM-DD"
