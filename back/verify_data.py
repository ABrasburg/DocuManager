"""
Script para verificar si hay datos problemáticos en la base del cliente.
Ejecutar con: python verify_data.py
"""
import sqlite3

def verify_comprobantes(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si hay valores que parecen problemáticos (0 o NULL donde no deberían)
    cursor.execute("""
        SELECT id, fecha_emision, punto_venta, numero_desde, numero_hasta, cod_autorizacion
        FROM comprobante
        WHERE punto_venta = 0
           OR numero_desde = 0
           OR numero_hasta = 0
           OR cod_autorizacion = 0
        ORDER BY id
    """)

    problematic = cursor.fetchall()

    if problematic:
        print(f"⚠️  Se encontraron {len(problematic)} comprobantes con valores en 0:")
        for row in problematic:
            print(f"  ID: {row[0]}, Fecha: {row[1]}, PV: {row[2]}, Desde: {row[3]}, Hasta: {row[4]}, CAE: {row[5]}")
        print("\nEstos registros pueden haberse cargado con errores por los separadores.")
        print("Se recomienda reprocesar estos archivos.")
    else:
        print("✅ No se encontraron problemas en los datos existentes.")

    conn.close()

if __name__ == "__main__":
    verify_data()
