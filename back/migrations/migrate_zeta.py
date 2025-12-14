"""
Script de migración para renombrar columnas en la tabla zeta
Renombra: gravado -> perfumeria, cuenta_corriente -> medicamentos_iva
"""
import sqlite3

def migrate_zeta_table():
    # Conectar a la base de datos
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:
        # Verificar si las columnas antiguas existen
        cursor.execute("PRAGMA table_info(zeta)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'perfumeria' in columns:
            print("✓ La tabla ya está migrada")
            return

        print("Iniciando migración de tabla zeta...")

        # 1. Crear tabla temporal con la nueva estructura
        cursor.execute("""
            CREATE TABLE zeta_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_ocho INTEGER DEFAULT -1,
                id_nueve INTEGER DEFAULT -1,
                fecha DATETIME NOT NULL,
                punto_de_venta INTEGER NOT NULL,
                numero INTEGER NOT NULL,
                ultimo_ticket INTEGER NOT NULL,
                exento FLOAT NOT NULL,
                iva FLOAT NOT NULL,
                perfumeria FLOAT NOT NULL,
                medicamentos_iva FLOAT NOT NULL,
                total FLOAT NOT NULL
            )
        """)

        # 2. Copiar datos de la tabla antigua a la nueva
        # gravado -> perfumeria, cuenta_corriente -> medicamentos_iva
        cursor.execute("""
            INSERT INTO zeta_new (
                id, id_ocho, id_nueve, fecha, punto_de_venta, numero,
                ultimo_ticket, exento, iva, perfumeria, medicamentos_iva, total
            )
            SELECT
                id, id_ocho, id_nueve, fecha, punto_de_venta, numero,
                ultimo_ticket, exento, iva, gravado, cuenta_corriente, total
            FROM zeta
        """)

        # 3. Borrar tabla antigua
        cursor.execute("DROP TABLE zeta")

        # 4. Renombrar tabla nueva
        cursor.execute("ALTER TABLE zeta_new RENAME TO zeta")

        # Confirmar cambios
        conn.commit()
        print("✓ Migración completada exitosamente")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error durante la migración: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_zeta_table()
