import { formatDateArgentina } from './formatDate';

describe('formatDateArgentina', () => {
  test('convierte YYYY-MM-DD a DD/MM/YYYY sin corrimiento horario', () => {
    expect(formatDateArgentina('2026-04-01')).toBe('01/04/2026');
  });

  test('mantiene fechas ya formateadas', () => {
    expect(formatDateArgentina('30/04/2026')).toBe('30/04/2026');
  });

  test('devuelve cadena vacia para valores invalidos', () => {
    expect(formatDateArgentina(null)).toBe('');
    expect(formatDateArgentina('fecha-invalida')).toBe('');
  });
});
