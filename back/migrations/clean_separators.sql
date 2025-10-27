-- Migración para limpiar separadores en campos numéricos de comprobantes
-- Ejecutar en la base de datos del cliente si hay datos con separadores

-- Nota: SQLite no tiene funciones REPLACE directas en UPDATE de manera nativa
-- Este script debe ejecutarse si se detectan problemas en los datos existentes

-- Para verificar si hay problemas (ejecutar primero):
-- SELECT id, punto_venta, numero_desde, numero_hasta, cod_autorizacion
-- FROM comprobante
-- WHERE CAST(punto_venta AS TEXT) LIKE '%-%'
--    OR CAST(punto_venta AS TEXT) LIKE '%/%'
--    OR CAST(numero_desde AS TEXT) LIKE '%-%'
--    OR CAST(numero_desde AS TEXT) LIKE '%/%';

-- Si se encuentran datos con separadores, contactar al desarrollador
-- para realizar la limpieza manualmente
