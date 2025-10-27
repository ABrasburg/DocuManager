# Migración de Fechas - Normalización a Formato ISO

## 🔍 Problema

La base de datos contiene fechas en diferentes formatos:
- `DD/MM/YYYY` (ej: 22/10/2025)
- `YYYY-MM-DD` (ej: 2025-10-22)

Esto causa problemas en los filtros porque SQLite compara como strings y el orden es incorrecto.

## ✅ Solución

1. **Script de migración**: Normaliza todas las fechas existentes a formato ISO (`YYYY-MM-DD`)
2. **Código actualizado**: Los nuevos archivos CSV se cargarán automáticamente con fechas normalizadas

---

## 📋 Instrucciones para Ejecutar la Migración

### ⚠️ IMPORTANTE: Hacer Backup

**Antes de ejecutar el script, hacer una copia de seguridad de la base de datos:**

```bash
# En Windows
copy data.db data.db.backup

# En Linux/Mac
cp data.db data.db.backup
```

### Paso 1: Ver los cambios (Dry-Run)

Primero ejecutá el script en modo "dry-run" para ver qué cambios se harían **sin aplicarlos**:

```bash
cd back
python migrate_dates.py
```

Esto mostrará:
- Cuántas fechas necesitan cambios
- Ejemplos de las conversiones que se harían
- Un resumen completo

### Paso 2: Aplicar los cambios

Si los cambios se ven correctos, ejecutá con el flag `--apply`:

```bash
python migrate_dates.py --apply
```

El script te pedirá confirmación antes de aplicar los cambios.

### Paso 3: Verificar

Después de la migración, verificá que:
1. Los filtros por fecha funcionen correctamente
2. Las fechas se muestran en el formato esperado
3. No hay datos perdidos

---

## 🔄 ¿Qué hace la migración?

El script:
1. Lee todas las fechas de la tabla `comprobante` (campos `fecha_emision` y `fecha_pago`)
2. Detecta el formato de cada fecha
3. Convierte todas las fechas al formato ISO: `YYYY-MM-DD`
4. Actualiza la base de datos

**Formatos soportados:**
- `DD/MM/YYYY` → `YYYY-MM-DD`
- `DD-MM-YYYY` → `YYYY-MM-DD`
- `YYYY/MM/DD` → `YYYY-MM-DD`
- `YYYY-MM-DD` → (sin cambios)

---

## 🚀 Después de la Migración

Una vez ejecutada la migración en producción:

1. **Todos los filtros funcionarán correctamente** porque todas las fechas estarán en el mismo formato
2. **Los nuevos comprobantes** que se carguen desde CSV se normalizarán automáticamente
3. **No hay cambios** visibles para el usuario final (las fechas se siguen mostrando igual en el frontend)

---

## ❓ Preguntas Frecuentes

**P: ¿Se perderán datos?**
R: No. El script solo cambia el formato de las fechas, no elimina ni modifica los valores.

**P: ¿Puedo deshacer los cambios?**
R: Sí, si hiciste el backup. Solo restaurá `data.db.backup`.

**P: ¿Tengo que parar el servidor?**
R: Recomendado. Para evitar conflictos, detené el backend antes de ejecutar la migración.

**P: ¿Cuánto tarda?**
R: Depende de la cantidad de registros, pero generalmente menos de 1 segundo para bases de datos pequeñas (<10,000 registros).

---

## 📞 Soporte

Si hay algún problema durante la migración, contactar al desarrollador antes de aplicar cambios.
