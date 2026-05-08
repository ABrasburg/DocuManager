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
