import { formatCurrency, formatNumber } from './formatNumber';

describe('formatNumber', () => {
  test('formatea numeros con separador argentino', () => {
    expect(formatNumber(1234.56)).toBe('1.234,56');
    expect(formatNumber(-1234.56)).toBe('-1.234,56');
  });

  test('normaliza valores vacios o invalidos', () => {
    expect(formatNumber(null)).toBe('0,00');
    expect(formatNumber(undefined)).toBe('0,00');
    expect(formatNumber(Number.NaN)).toBe('0,00');
  });
});

describe('formatCurrency', () => {
  test('agrega signo pesos y conserva negativos antes del simbolo', () => {
    expect(formatCurrency(1234.56)).toBe('$1.234,56');
    expect(formatCurrency(-1234.56)).toBe('-$1.234,56');
  });
});
