-- Migración para agregar tipo de comprobante 2: Nota de Débito
-- Fecha: 2025-12-14
-- Descripción: Agrega el tipo de comprobante 2 (Nota de Débito) a la tabla tipo_comprobante
--             La Nota de Débito se comporta como una factura (valores positivos)

-- IMPORTANTE: Este script es idempotente, puede ejecutarse múltiples veces sin causar errores

-- Para SQLite (desarrollo):
-- Verificar primero si ya existe el tipo de comprobante 2
-- Si no existe, insertarlo

INSERT INTO tipo_comprobante (tipo_comprobante, nombre)
SELECT 2, 'Nota de Débito'
WHERE NOT EXISTS (
    SELECT 1 FROM tipo_comprobante WHERE tipo_comprobante = 2
);

-- Verificar el resultado de la migración (opcional, para validar):
-- SELECT * FROM tipo_comprobante ORDER BY tipo_comprobante;

-- Resultado esperado:
-- id | tipo_comprobante | nombre
-- ---+------------------+------------------
-- 1  | 1                | Factura
-- 2  | 3                | Nota de Crédito
-- 3  | 2                | Nota de Débito
