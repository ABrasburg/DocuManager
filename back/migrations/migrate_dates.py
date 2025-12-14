"""
Script para normalizar todas las fechas en la base de datos a formato ISO (YYYY-MM-DD).
Esto soluciona el problema de fechas en múltiples formatos que causan problemas en los filtros.

IMPORTANTE: Hacer backup de la base de datos antes de ejecutar.
Uso: python migrate_dates.py
"""
import sqlite3
from datetime import datetime
import sys

def parse_date(date_str):
    """
    Intenta parsear una fecha en diferentes formatos y retorna formato ISO (YYYY-MM-DD).
    Formatos soportados:
    - DD/MM/YYYY (ej: 22/10/2025)
    - YYYY-MM-DD (ej: 2025-10-22)
    - DD-MM-YYYY (ej: 22-10-2025)
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # Si ya está en formato ISO, retornar tal cual
    if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
        try:
            # Validar que sea una fecha válida
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            pass

    # Intentar parsear diferentes formatos
    formats = [
        '%d/%m/%Y',  # 22/10/2025
        '%d-%m-%Y',  # 22-10-2025
        '%Y/%m/%d',  # 2025/10/22
        '%Y-%m-%d',  # 2025-10-22
    ]

    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            continue

    print(f"⚠️  No se pudo parsear la fecha: '{date_str}'")
    return date_str  # Retornar sin cambios si no se puede parsear

def migrate_dates(db_path='data.db', dry_run=True):
    """
    Migra todas las fechas en la tabla comprobante al formato ISO.

    Args:
        db_path: Ruta a la base de datos
        dry_run: Si es True, solo muestra los cambios sin aplicarlos
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener todos los comprobantes con sus fechas
    cursor.execute("""
        SELECT id, fecha_emision, fecha_pago
        FROM comprobante
        ORDER BY id
    """)

    comprobantes = cursor.fetchall()

    if not comprobantes:
        print("✅ No hay comprobantes en la base de datos")
        conn.close()
        return

    cambios_emision = []
    cambios_pago = []

    print(f"\n{'='*80}")
    print(f"Analizando {len(comprobantes)} comprobantes...")
    print(f"{'='*80}\n")

    for comp_id, fecha_emision, fecha_pago in comprobantes:
        # Procesar fecha_emision
        if fecha_emision:
            fecha_normalizada = parse_date(fecha_emision)
            if fecha_normalizada != fecha_emision:
                cambios_emision.append((comp_id, fecha_emision, fecha_normalizada))

        # Procesar fecha_pago
        if fecha_pago:
            fecha_normalizada = parse_date(fecha_pago)
            if fecha_normalizada != fecha_pago:
                cambios_pago.append((comp_id, fecha_pago, fecha_normalizada))

    # Mostrar resumen
    print(f"📊 Resumen de cambios:")
    print(f"   - Fechas de emisión a normalizar: {len(cambios_emision)}")
    print(f"   - Fechas de pago a normalizar: {len(cambios_pago)}")
    print()

    if cambios_emision:
        print("Cambios en fecha_emision:")
        for comp_id, old_date, new_date in cambios_emision[:10]:  # Mostrar primeros 10
            print(f"   ID {comp_id}: '{old_date}' → '{new_date}'")
        if len(cambios_emision) > 10:
            print(f"   ... y {len(cambios_emision) - 10} más")
        print()

    if cambios_pago:
        print("Cambios en fecha_pago:")
        for comp_id, old_date, new_date in cambios_pago[:10]:
            print(f"   ID {comp_id}: '{old_date}' → '{new_date}'")
        if len(cambios_pago) > 10:
            print(f"   ... y {len(cambios_pago) - 10} más")
        print()

    if not cambios_emision and not cambios_pago:
        print("✅ Todas las fechas ya están en formato correcto (YYYY-MM-DD)")
        conn.close()
        return

    if dry_run:
        print(f"\n{'='*80}")
        print("🔍 MODO DRY-RUN: No se aplicaron cambios.")
        print("Para aplicar los cambios, ejecuta:")
        print("   python migrate_dates.py --apply")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'='*80}")
        print("⚠️  ¿Aplicar estos cambios? (s/n): ", end='')
        respuesta = input().lower().strip()

        if respuesta != 's':
            print("❌ Migración cancelada")
            conn.close()
            return

        # Aplicar cambios
        print("\n🔄 Aplicando cambios...")

        for comp_id, _, fecha_normalizada in cambios_emision:
            cursor.execute("""
                UPDATE comprobante
                SET fecha_emision = ?
                WHERE id = ?
            """, (fecha_normalizada, comp_id))

        for comp_id, _, fecha_normalizada in cambios_pago:
            cursor.execute("""
                UPDATE comprobante
                SET fecha_pago = ?
                WHERE id = ?
            """, (fecha_normalizada, comp_id))

        conn.commit()
        print(f"✅ Migración completada exitosamente")
        print(f"   - {len(cambios_emision)} fechas de emisión actualizadas")
        print(f"   - {len(cambios_pago)} fechas de pago actualizadas")
        print(f"{'='*80}\n")

    conn.close()

if __name__ == "__main__":
    import sys

    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MIGRACIÓN DE FECHAS - DocuManager                         ║
║                                                                              ║
║  Este script normaliza todas las fechas al formato ISO (YYYY-MM-DD)         ║
║  para que los filtros funcionen correctamente.                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Verificar si se pasó el flag --apply
    apply_changes = '--apply' in sys.argv

    if not apply_changes:
        print("⚠️  MODO DRY-RUN: Solo se mostrarán los cambios, no se aplicarán.\n")
    else:
        print("⚠️  IMPORTANTE: Asegúrate de tener un backup de data.db antes de continuar.\n")

    migrate_dates(db_path='data.db', dry_run=not apply_changes)
