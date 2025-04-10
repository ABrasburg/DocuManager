import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import React, { useState, useEffect } from 'react';

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
  handleSave: (comprobante: Comprobante) => void;
}

const ComprobantePopup: React.FC<Props> = ({ comprobante, onClose, open, handleSave }) => {
  const [editableComprobante, setEditableComprobante] = useState<Comprobante | null>(null);

  useEffect(() => {
    if (comprobante) {
      setEditableComprobante(comprobante);
    }
  }, [comprobante]);

  const handleChange = <K extends keyof Comprobante>(field: K, value: Comprobante[K]) => {
    if (editableComprobante) {
      setEditableComprobante({
        ...editableComprobante,
        [field]: value,
      });
    }
  };

  const handleNestedChange = <K extends keyof Comprobante, NK extends keyof Comprobante[K]>(
    field: K,
    nestedField: NK,
    value: Comprobante[K][NK]
  ) => {
    if (editableComprobante && typeof editableComprobante[field] === 'object') {
      setEditableComprobante({
        ...editableComprobante,
        [field]: {
          ...(editableComprobante[field] as any),
          [nestedField]: value,
        },
      });
    }
  };

  return (
    <Popup open={open} onClose={onClose} modal nested>
      <div className="p-6 bg-white rounded-xl shadow-xl max-w-xl w-full">
        <h2 className="text-xl font-semibold mb-4 text-center border-b pb-2">
          Editar Comprobante
        </h2>

        {editableComprobante ? (
          <form className="space-y-4 text-sm text-gray-700">
            <div>
              <label className="block font-medium">Fecha emisión:</label>
              <input
                type="text"
                value={editableComprobante.fecha_emision}
                onChange={(e) => handleChange('fecha_emision', e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block font-medium">Punto de venta:</label>
                <input
                  type="number"
                  value={editableComprobante.punto_venta}
                  onChange={(e) => handleChange('punto_venta', Number(e.target.value))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block font-medium">Tipo cambio:</label>
                <input
                  type="number"
                  value={editableComprobante.tipo_cambio}
                  onChange={(e) => handleChange('tipo_cambio', Number(e.target.value))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block font-medium">Número desde:</label>
                <input
                  type="number"
                  value={editableComprobante.numero_desde}
                  onChange={(e) => handleChange('numero_desde', Number(e.target.value))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block font-medium">Número hasta:</label>
                <input
                  type="number"
                  value={editableComprobante.numero_hasta}
                  onChange={(e) => handleChange('numero_hasta', Number(e.target.value))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label className="block font-medium">Cod. autorización:</label>
              <input
                type="text"
                value={editableComprobante.cod_autorizacion}
                onChange={(e) => handleChange('cod_autorizacion', e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>

            <div>
              <label className="block font-medium">Moneda:</label>
              <input
                type="text"
                value={editableComprobante.moneda}
                onChange={(e) => handleChange('moneda', e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>

            <div>
              <label className="block font-medium">Total:</label>
              <input
                type="number"
                value={editableComprobante.total}
                onChange={(e) => handleChange('total', Number(e.target.value))}
                className="w-full border rounded px-3 py-2"
              />
            </div>

            <div>
              <label className="block font-medium">Emisor:</label>
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Denominación"
                  value={editableComprobante.emisor.denominacion}
                  onChange={(e) => handleNestedChange('emisor', 'denominacion', e.target.value)}
                  className="w-full border rounded px-3 py-2"
                />
                <input
                  type="text"
                  placeholder="CUIT"
                  value={editableComprobante.emisor.cuit}
                  onChange={(e) => handleNestedChange('emisor', 'cuit', e.target.value)}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label className="block font-medium">Tipo de comprobante:</label>
              <input
                type="text"
                value={editableComprobante.tipo_comprobante.nombre}
                onChange={(e) => handleNestedChange('tipo_comprobante', 'nombre', e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
          </form>
        ) : (
          <p className="text-red-500">No hay datos disponibles para este comprobante.</p>
        )}

        <div className="mt-4 flex justify-between">
          <button
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            onClick={onClose}
          >
            Cerrar
          </button>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            onClick={() => {
              handleSave(editableComprobante as Comprobante);
              onClose();
            }}
          >
            Guardar
          </button>
        </div>
      </div>
    </Popup>
  );
};

export default ComprobantePopup;
