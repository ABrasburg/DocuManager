# Migración: Agregar Tipo de Comprobante 2 - Nota de Débito

**Fecha:** 2025-12-14
**Descripción:** Agrega el tipo de comprobante 2 (Nota de Débito) a la base de datos de producción.

## Comportamiento

La Nota de Débito se comporta como una factura:
- ✅ Suma al total de la cuenta corriente (valores positivos)
- ❌ NO resta como la Nota de Crédito (tipo 3)

## Tipos de Comprobante

Después de la migración tendrás:

| ID | Tipo | Nombre | Comportamiento |
|---|---|---|---|
| 1 | Factura | Suma (valores positivos) |
| 2 | Nota de Débito | Suma (valores positivos) |
| 3 | Nota de Crédito | Resta (valores negativos) |

## Métodos de Ejecución

### Opción 1: Script Python (Recomendado)

```bash
# Desde el directorio /back
cd /Users/agustin/Desktop/Proyectos/DocuManager/back

# Ejecutar el script de migración
python3 migrations/migrate_add_nota_debito.py
```

Para producción con base de datos en otra ubicación:
```bash
DB_PATH=/path/to/production/data.db python3 migrations/migrate_add_nota_debito.py
```

### Opción 2: SQL Directo

```bash
# Para SQLite
sqlite3 data.db < migrations/add_nota_debito_tipo_comprobante.sql

# Para PostgreSQL (si aplica en producción)
psql -d nombre_base_datos -f migrations/add_nota_debito_tipo_comprobante.sql
```

## Verificación

Después de ejecutar la migración, verifica que se agregó correctamente:

```sql
SELECT * FROM tipo_comprobante ORDER BY tipo_comprobante;
```

Deberías ver:
```
id | tipo_comprobante | nombre
---+------------------+------------------
1  | 1                | Factura
2  | 3                | Nota de Crédito
3  | 2                | Nota de Débito
```

## Seguridad

✅ Esta migración es **idempotente**: puede ejecutarse múltiples veces sin causar errores
✅ No afecta datos existentes
✅ Solo agrega un nuevo registro si no existe

## Rollback

Si necesitas revertir la migración:

```sql
DELETE FROM tipo_comprobante WHERE tipo_comprobante = 2;
```

**NOTA:** Solo hazlo si NO has creado comprobantes con tipo 2.
