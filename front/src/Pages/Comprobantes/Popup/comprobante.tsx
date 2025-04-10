import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import React from 'react';

interface Comprobante {
    id: number;
    fecha_emision: string;
    punto_venta: number;
    numero_desde: number;
    numero_hasta: number;
    cod_autorizacion: string;
    tipo_cambio: number;
    moneda: string;
    total: number;
    emisor: {
      cuit: string;
      denominacion: string;
    };
    tipo_comprobante: {
      nombre: string;
    };
  }

interface Props {
  open : boolean;
  comprobante: Comprobante | null;
  onClose: () => void;
}

const ComprobantePopup: React.FC<Props> = ({ comprobante, onClose, open }) => {
  return (
     <Popup open={open} onClose={onClose} modal nested>
      <div style={{ padding: '20px', maxWidth: '500px' }}>
        <h3>Detalle del Comprobante</h3>
        {comprobante ? (
          <>
            <p><strong>Fecha emisión:</strong> {comprobante.fecha_emision}</p>
            <p><strong>Punto de venta:</strong> {comprobante.punto_venta}</p>
            <p><strong>Número desde:</strong> {comprobante.numero_desde}</p>
            <p><strong>Número hasta:</strong> {comprobante.numero_hasta}</p>
            <p><strong>Cod. autorización:</strong> {comprobante.cod_autorizacion}</p>
            <p><strong>Tipo cambio:</strong> {comprobante.tipo_cambio}</p>
            <p><strong>Moneda:</strong> {comprobante.moneda}</p>
            <p><strong>Total:</strong> ${comprobante.total}</p>
            <p><strong>Emisor:</strong> {comprobante.emisor.denominacion} ({comprobante.emisor.cuit})</p>
            <p><strong>Tipo de comprobante:</strong> {comprobante.tipo_comprobante.nombre}</p>
          </>
        ) : (
          <p>No hay datos disponibles para este comprobante.</p>
        )}
      </div>
    </Popup>
  );
};

export default ComprobantePopup;
