# Migraciones de Base de Datos

Esta carpeta contiene todos los scripts de migración y mantenimiento de la base de datos del proyecto DocuManager.

## Ubicación

Todos los scripts deben ejecutarse desde el directorio `/back`:

```bash
cd /Users/agustin/Desktop/Proyectos/DocuManager/back
```

## Scripts de Migración Disponibles

### 1. migrate_add_nota_debito.py
**Descripción:** Agrega el tipo de comprobante 2 (Nota de Débito) a la base de datos.

**Uso:**
```bash
python3 migrations/migrate_add_nota_debito.py
```

**Detalles:** Ver [README_NOTA_DEBITO.md](README_NOTA_DEBITO.md)

**Características:**
- ✅ Idempotente (puede ejecutarse múltiples veces)
- ✅ No afecta datos existentes
- ✅ Muestra confirmación de resultados

---

### 2. migrate_zeta.py
**Descripción:** Migración de columnas en la tabla zeta.

**Cambios:**
- Renombra: `gravado` → `perfumeria`
- Renombra: `cuenta_corriente` → `medicamentos_iva`

**Uso:**
```bash
python3 migrations/migrate_zeta.py
```

**Características:**
- ⚠️ Modifica estructura de tabla
- ✅ Verifica si ya fue aplicada
- ✅ Copia datos preservando información

---

### 3. migrate_dates.py
**Descripción:** Normaliza todas las fechas en la base de datos a formato ISO (YYYY-MM-DD).

**Problema que resuelve:** Fechas en múltiples formatos que causan problemas en los filtros.

**Uso:**
```bash
python3 migrations/migrate_dates.py
```

**Características:**
- ⚠️ Modifica datos existentes
- ⚠️ **HACER BACKUP** antes de ejecutar
- ✅ Soporta múltiples formatos de entrada
- ✅ Normaliza a formato ISO estándar

**Formatos soportados:**
- DD/MM/YYYY (ej: 22/10/2025)
- YYYY-MM-DD (ej: 2025-10-22)
- DD-MM-YYYY (ej: 22-10-2025)

---

### 4. verify_data.py
**Descripción:** Script de verificación para detectar datos problemáticos en comprobantes.

**Uso:**
```bash
python3 migrations/verify_data.py
```

**Qué verifica:**
- Comprobantes con punto_venta = 0
- Comprobantes con numero_desde = 0
- Comprobantes con numero_hasta = 0
- Comprobantes con cod_autorizacion = 0

**Características:**
- ✅ No modifica datos (solo lectura)
- ✅ Genera reporte de problemas encontrados
- ✅ Seguro ejecutar en cualquier momento

---

## Scripts SQL

### add_nota_debito_tipo_comprobante.sql
Versión SQL del script de migración para agregar Nota de Débito.

**Uso:**
```bash
sqlite3 data.db < migrations/add_nota_debito_tipo_comprobante.sql
```

### clean_separators.sql
Script de verificación para detectar separadores problemáticos en campos numéricos.

---

## Recomendaciones

### Antes de Ejecutar Migraciones en Producción:

1. **Hacer backup de la base de datos:**
   ```bash
   cp data.db data.db.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Probar en desarrollo primero:**
   - Ejecutar en base de datos de desarrollo
   - Verificar resultados
   - Confirmar que todo funciona correctamente

3. **Documentar la ejecución:**
   - Anotar fecha y hora de ejecución
   - Guardar output del script
   - Verificar estado post-migración

### Orden Recomendado de Ejecución (para nuevas instalaciones):

1. `migrate_zeta.py` - Si se necesita migrar estructura de zeta
2. `migrate_dates.py` - Si hay problemas con formatos de fecha
3. `migrate_add_nota_debito.py` - Para agregar Nota de Débito
4. `verify_data.py` - Verificación final

### Para Base de Datos en Otra Ubicación:

```bash
DB_PATH=/ruta/a/data.db python3 migrations/script_name.py
```

---

## Estado de Migraciones

| Migración | Ejecutada | Fecha | Notas |
|-----------|-----------|-------|-------|
| migrate_add_nota_debito.py | ✅ | 2025-12-14 | Tipo 2 agregado |
| migrate_zeta.py | - | - | - |
| migrate_dates.py | - | - | - |

**Nota:** Actualizar esta tabla después de ejecutar cada migración en producción.
