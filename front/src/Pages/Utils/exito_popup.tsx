import React, { useEffect } from 'react';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

interface ExitoPopupProps {
  open: boolean;
  onClose: () => void;
  texto: string;
}

const ExitoPopup: React.FC<ExitoPopupProps> = ({ open, onClose, texto }) => {
  useEffect(() => {
    if (open) {
      const timer = setTimeout(() => {
        onClose();
      }, 3000); // cerrar después de 3s
      return () => clearTimeout(timer);
    }
  }, [open, onClose]);

  return (
    <Popup open={open} onClose={onClose} modal nested>
      <div className="relative p-4 text-center">
        <h2 className="text-green-600 text-lg font-semibold">¡Éxito!</h2>
        <p className="mt-2">{texto}</p>
        {/* Botón para cerrar */}
        <button
          className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          onClick={onClose}
        >
          Cerrar
        </button>
      </div>
    </Popup>
  );
};

export default ExitoPopup;