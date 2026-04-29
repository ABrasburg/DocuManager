"""
Script de integración: une Mighetti.db y SAS.db en una sola data.db con soporte multi-farmacia.

Uso:
    python integrate_farmacias.py --mighetti /path/Mighetti.db --sas /path/SAS.db --output /path/data.db
"""
import sqlite3
import argparse
import shutil
import os


FARMACIAS = [
    {"nombre": "Mighetti"},
    {"nombre": "SAS"},
]


def migrate_sas_zeta(cursor):
    """Migra la tabla zeta de SAS al esquema nuevo (gravado->perfumeria, cuenta_corriente->medicamentos_iva)."""
    cursor.execute("PRAGMA table_info(zeta)")
    columns = [col[1] for col in cursor.fetchall()]
    if "gravado" in columns:
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
        cursor.execute("""
            INSERT INTO zeta_new
                (id, id_ocho, id_nueve, fecha, punto_de_venta, numero,
                 ultimo_ticket, exento, iva, perfumeria, medicamentos_iva, total)
            SELECT
                id, id_ocho, id_nueve, fecha, punto_de_venta, numero,
                ultimo_ticket, exento, iva, gravado, cuenta_corriente, total
            FROM zeta
        """)
        cursor.execute("DROP TABLE zeta")
        cursor.execute("ALTER TABLE zeta_new RENAME TO zeta")
        print("  [SAS] Tabla zeta migrada al esquema nuevo")


def create_output_schema(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS farmacia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS tipo_comprobante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_comprobante INTEGER NOT NULL,
            nombre VARCHAR NOT NULL,
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id),
            UNIQUE (tipo_comprobante, farmacia_id)
        );

        CREATE TABLE IF NOT EXISTS emisor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_doc VARCHAR NOT NULL,
            cuit INTEGER NOT NULL,
            denominacion VARCHAR NOT NULL,
            cuenta_corriente BOOLEAN NOT NULL,
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id),
            UNIQUE (cuit, farmacia_id)
        );

        CREATE TABLE IF NOT EXISTS archivos_comprobantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo VARCHAR NOT NULL,
            numero_hasta INTEGER,
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id)
        );

        CREATE TABLE IF NOT EXISTS comprobante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_emision VARCHAR NOT NULL,
            punto_venta INTEGER NOT NULL,
            numero_desde INTEGER NOT NULL,
            numero_hasta INTEGER NOT NULL,
            cod_autorizacion INTEGER NOT NULL,
            tipo_cambio FLOAT NOT NULL,
            moneda VARCHAR NOT NULL,
            neto_gravado FLOAT NOT NULL,
            neto_no_gravado FLOAT,
            exento FLOAT,
            otros_tributos FLOAT NOT NULL,
            iva FLOAT NOT NULL,
            total FLOAT NOT NULL,
            fecha_pago VARCHAR,
            numero_ticket VARCHAR,
            emisor_id INTEGER REFERENCES emisor(id),
            tipo_comprobante_id INTEGER REFERENCES tipo_comprobante(id),
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id)
        );

        CREATE TABLE IF NOT EXISTS idzeta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contador INTEGER,
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id)
        );

        CREATE TABLE IF NOT EXISTS zeta (
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
            total FLOAT NOT NULL,
            farmacia_id INTEGER NOT NULL REFERENCES farmacia(id)
        );
    """)


def import_farmacia(out_conn, src_path, farmacia_nombre, migrate_zeta_fn=None):
    print(f"\n[{farmacia_nombre}] Importando desde {src_path}...")

    src_conn = sqlite3.connect(src_path)
    src_conn.row_factory = sqlite3.Row
    src = src_conn.cursor()

    if migrate_zeta_fn:
        migrate_zeta_fn(src)
        src_conn.commit()

    out = out_conn.cursor()

    # Obtener farmacia_id
    out.execute("SELECT id FROM farmacia WHERE nombre = ?", (farmacia_nombre,))
    farmacia_id = out.fetchone()[0]

    # tipo_comprobante: mapeo viejo id -> nuevo id
    tipo_id_map = {}
    src.execute("SELECT * FROM tipo_comprobante")
    for row in src.fetchall():
        out.execute(
            "INSERT OR IGNORE INTO tipo_comprobante (tipo_comprobante, nombre, farmacia_id) VALUES (?,?,?)",
            (row["tipo_comprobante"], row["nombre"], farmacia_id)
        )
        out.execute(
            "SELECT id FROM tipo_comprobante WHERE tipo_comprobante=? AND farmacia_id=?",
            (row["tipo_comprobante"], farmacia_id)
        )
        tipo_id_map[row["id"]] = out.fetchone()[0]

    # emisor: mapeo viejo id -> nuevo id
    emisor_id_map = {}
    src.execute("SELECT * FROM emisor")
    for row in src.fetchall():
        out.execute(
            "INSERT OR IGNORE INTO emisor (tipo_doc, cuit, denominacion, cuenta_corriente, farmacia_id) VALUES (?,?,?,?,?)",
            (row["tipo_doc"], row["cuit"], row["denominacion"], row["cuenta_corriente"], farmacia_id)
        )
        out.execute(
            "SELECT id FROM emisor WHERE cuit=? AND farmacia_id=?",
            (row["cuit"], farmacia_id)
        )
        emisor_id_map[row["id"]] = out.fetchone()[0]

    # comprobantes
    src.execute("SELECT * FROM comprobante")
    for row in src.fetchall():
        out.execute("""
            INSERT INTO comprobante
                (fecha_emision, punto_venta, numero_desde, numero_hasta, cod_autorizacion,
                 tipo_cambio, moneda, neto_gravado, neto_no_gravado, exento, otros_tributos,
                 iva, total, fecha_pago, numero_ticket, emisor_id, tipo_comprobante_id, farmacia_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            row["fecha_emision"], row["punto_venta"], row["numero_desde"], row["numero_hasta"],
            row["cod_autorizacion"], row["tipo_cambio"], row["moneda"], row["neto_gravado"],
            row["neto_no_gravado"], row["exento"], row["otros_tributos"], row["iva"], row["total"],
            row["fecha_pago"], row["numero_ticket"],
            emisor_id_map.get(row["emisor_id"]),
            tipo_id_map.get(row["tipo_comprobante_id"]),
            farmacia_id
        ))

    # archivos_comprobantes
    src.execute("SELECT * FROM archivos_comprobantes")
    for row in src.fetchall():
        out.execute(
            "INSERT INTO archivos_comprobantes (nombre_archivo, numero_hasta, farmacia_id) VALUES (?,?,?)",
            (row["nombre_archivo"], row["numero_hasta"], farmacia_id)
        )

    # idzeta
    src.execute("SELECT * FROM idzeta")
    for row in src.fetchall():
        out.execute(
            "INSERT INTO idzeta (contador, farmacia_id) VALUES (?,?)",
            (row["contador"], farmacia_id)
        )

    # zeta
    src.execute("SELECT * FROM zeta")
    for row in src.fetchall():
        out.execute("""
            INSERT INTO zeta
                (id_ocho, id_nueve, fecha, punto_de_venta, numero, ultimo_ticket,
                 exento, iva, perfumeria, medicamentos_iva, total, farmacia_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            row["id_ocho"], row["id_nueve"], row["fecha"], row["punto_de_venta"],
            row["numero"], row["ultimo_ticket"], row["exento"], row["iva"],
            row["perfumeria"], row["medicamentos_iva"], row["total"], farmacia_id
        ))

    src_conn.close()

    out.execute("SELECT COUNT(*) FROM comprobante WHERE farmacia_id=?", (farmacia_id,))
    print(f"  Comprobantes importados: {out.fetchone()[0]}")
    out.execute("SELECT COUNT(*) FROM zeta WHERE farmacia_id=?", (farmacia_id,))
    print(f"  Zetas importadas: {out.fetchone()[0]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mighetti", required=True)
    parser.add_argument("--sas", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if os.path.exists(args.output):
        backup = args.output + ".backup"
        shutil.copy2(args.output, backup)
        print(f"Backup creado en {backup}")
        os.remove(args.output)

    out_conn = sqlite3.connect(args.output)
    out_conn.execute("PRAGMA foreign_keys = ON")

    create_output_schema(out_conn.cursor())

    out = out_conn.cursor()
    for f in FARMACIAS:
        out.execute("INSERT INTO farmacia (nombre) VALUES (?)", (f["nombre"],))
    out_conn.commit()

    import_farmacia(out_conn, args.mighetti, "Mighetti")
    out_conn.commit()

    import_farmacia(out_conn, args.sas, "SAS", migrate_zeta_fn=migrate_sas_zeta)
    out_conn.commit()

    out_conn.close()
    print(f"\n=== Integración completa -> {args.output} ===")


if __name__ == "__main__":
    main()
