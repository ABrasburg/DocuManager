/**
 * Formatea una fecha al formato argentino DD/MM/YYYY
 * @param dateString - Fecha en formato YYYY-MM-DD, DD/MM/YYYY o timestamp
 * @returns Fecha formateada en DD/MM/YYYY o cadena vacía si es inválida
 */
export const formatDateArgentina = (dateString: string | number | null | undefined): string => {
  if (!dateString) return '';

  try {
    let date: Date;

    // Si es un número (timestamp)
    if (typeof dateString === 'number') {
      date = new Date(dateString);
    }
    // Si es un string
    else {
      // Si ya está en formato DD/MM/YYYY, devolverlo tal cual
      if (/^\d{2}\/\d{2}\/\d{4}$/.test(dateString)) {
        return dateString;
      }

      // Si está en formato YYYY-MM-DD (sin hora)
      if (/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
        date = new Date(dateString + 'T00:00:00'); // Agregar hora para evitar problemas de zona horaria
      } else {
        // Para cualquier otro formato (incluyendo ISO con hora: YYYY-MM-DDTHH:mm:ss)
        date = new Date(dateString);
      }
    }

    // Verificar que la fecha sea válida
    if (isNaN(date.getTime())) {
      return '';
    }

    // Formatear a DD/MM/YYYY
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    return `${day}/${month}/${year}`;
  } catch (error) {
    return '';
  }
};
