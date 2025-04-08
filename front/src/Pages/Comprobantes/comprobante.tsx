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
  open: boolean;
  onClose: () => void;
  comprobante: Comprobante | null;
}

const ComprobantePopup: React.FC<Props> = ({ comprobante, onClose, open }) => {
  return (
    <Popup open={open} onClose={onClose} modal nested>
      <div className="p-6 bg-white rounded-xl shadow-xl max-w-xl w-full">
        <h2 className="text-xl font-semibold mb-4 text-center border-b pb-2">
          Detalle del Comprobante
        </h2>

        {comprobante ? (
          <div className="space-y-2 text-sm text-gray-700">
            <p><span className="font-medium">Fecha emisión:</span> {comprobante.fecha_emision}</p>
            <p><span className="font-medium">Punto de venta:</span> {comprobante.punto_venta}</p>
            <p><span className="font-medium">Número desde:</span> {comprobante.numero_desde}</p>
            <p><span className="font-medium">Número hasta:</span> {comprobante.numero_hasta}</p>
            <p><span className="font-medium">Cod. autorización:</span> {comprobante.cod_autorizacion}</p>
            <p><span className="font-medium">Tipo cambio:</span> {comprobante.tipo_cambio}</p>
            <p><span className="font-medium">Moneda:</span> {comprobante.moneda}</p>
            <p><span className="font-medium">Total:</span> ${comprobante.total}</p>
            <p><span className="font-medium">Emisor:</span> {comprobante.emisor.denominacion} ({comprobante.emisor.cuit})</p>
            <p><span className="font-medium">Tipo de comprobante:</span> {comprobante.tipo_comprobante.nombre}</p>
          </div>
        ) : (
          <p className="text-red-500">No hay datos disponibles para este comprobante.</p>
        )}

        <div className="mt-6 flex justify-center">
          <button
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            onClick={onClose}
          >
            Cerrar
          </button>
        </div>
      </div>
    </Popup>
  );
};

export default ComprobantePopup;
