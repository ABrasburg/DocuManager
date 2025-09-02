/**
 * Formatea un número con el símbolo $ adelante, separador de miles con punto
 * y manejo correcto de números negativos
 * Ejemplos:
 * 1234.56 → $1.234,56
 * -1234.56 → -$1.234,56
 * 0 → $0,00
 */
export const formatCurrency = (num: number | null | undefined): string => {
  if (num === null || num === undefined || isNaN(num)) {
    return '$0,00';
  }

  const isNegative = num < 0;
  const absoluteNum = Math.abs(num);

  // Formatear el número con separador de miles (punto) y decimales (coma)
  const formatted = new Intl.NumberFormat('de-DE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(absoluteNum);

  // Devolver con el signo negativo adelante del $
  return isNegative ? `-$${formatted}` : `$${formatted}`;
};

/**
 * Formatea un número sin el símbolo $, solo con separador de miles
 * Ejemplos:
 * 1234.56 → 1.234,56
 * -1234.56 → -1.234,56
 */
export const formatNumber = (num: number | null | undefined): string => {
  if (num === null || num === undefined || isNaN(num)) {
    return '0,00';
  }

  return new Intl.NumberFormat('de-DE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
};