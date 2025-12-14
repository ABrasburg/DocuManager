#!/usr/bin/env python3
"""
Script de migración para agregar tipo de comprobante 2: Nota de Débito
Fecha: 2025-12-14
Descripción: Agrega el tipo de comprobante 2 (Nota de Débito) a la tabla tipo_comprobante
             La Nota de Débito se comporta como una factura (valores positivos)
"""
import sqlite3
import os

def migrate_add_nota_debito():
    # Conectar a la base de datos
    db_path = os.getenv('DB_PATH', 'data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Iniciando migración: Agregar Nota de Débito (tipo 2)...")

        # Verificar si ya existe el tipo de comprobante 2
        cursor.execute("""
            SELECT COUNT(*) FROM tipo_comprobante WHERE tipo_comprobante = 2
        """)
        count = cursor.fetchone()[0]

        if count > 0:
            print("✓ El tipo de comprobante 2 (Nota de Débito) ya existe")
            # Mostrar el registro existente
            cursor.execute("""
                SELECT * FROM tipo_comprobante WHERE tipo_comprobante = 2
            """)
            existing = cursor.fetchone()
            print(f"  Registro existente: id={existing[0]}, tipo_comprobante={existing[1]}, nombre={existing[2]}")
            return

        # Insertar el nuevo tipo de comprobante
        cursor.execute("""
            INSERT INTO tipo_comprobante (tipo_comprobante, nombre)
            VALUES (2, 'Nota de Débito')
        """)

        # Confirmar cambios
        conn.commit()
        print("✓ Tipo de comprobante 2 (Nota de Débito) agregado exitosamente")

        # Mostrar todos los tipos de comprobante
        cursor.execute("SELECT * FROM tipo_comprobante ORDER BY tipo_comprobante")
        tipos = cursor.fetchall()
        print("\nTipos de comprobante actuales:")
        print("id | tipo_comprobante | nombre")
        print("---+------------------+------------------")
        for tipo in tipos:
            print(f"{tipo[0]:<3}| {tipo[1]:<17}| {tipo[2]}")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error durante la migración: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_add_nota_debito()
