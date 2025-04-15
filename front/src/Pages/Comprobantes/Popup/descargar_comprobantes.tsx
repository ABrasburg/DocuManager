import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import React, { useState, useEffect } from 'react';

interface Props {
    open: boolean;
    onClose: () => void;
}

const DescargarComprobantes: React.FC<Props> = ({ open, onClose }) => {
    const [fechaInicio, setFechaInicio] = useState<string>('');
    const [fechaFin, setFechaFin] = useState<string>('');

    const handleDownload = async () => {
        try {
            const params = new URLSearchParams({
                fecha_inicio: fechaInicio,
                fecha_fin: fechaFin,
            });
    
            const response = await fetch(`http://localhost:9000/comprobantes/download?${params.toString()}`, {
                method: 'GET',
            });
    
            if (!response.ok) {
                throw new Error('Error al descargar los comprobantes');
            }
    
            const blob = await response.blob();
    
            // Obtener nombre de archivo desde el header 'Content-Disposition'
            const disposition = response.headers.get("Content-Disposition");
            let filename = "comprobantes.csv";
    
            if (disposition && disposition.includes("filename=")) {
                const match = disposition.match(/filename="?([^"]+)"?/);
                if (match?.[1]) {
                    filename = match[1];
                }
            }
    
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error en la descarga:', error);
        }
    };    

    const handleFechaInicioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFechaInicio(e.target.value);
    };

    const handleFechaFinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFechaFin(e.target.value);
    };

    return (
        <Popup open={open} onClose={onClose} modal>
            <div className="p-6">
                <h2 className="text-lg font-bold mb-4">Descargar Comprobantes</h2>
                <form onSubmit={(e) => e.preventDefault()} className="flex flex-col gap-4">
                    <label>
                        Fecha Inicio:
                        <input
                            type="date"
                            value={fechaInicio}
                            onChange={handleFechaInicioChange}
                            className="border rounded p-2 w-full"
                        />
                    </label>
                    <label>
                        Fecha Fin:
                        <input
                            type="date"
                            value={fechaFin}
                            onChange={handleFechaFinChange}
                            className="border rounded p-2 w-full"
                        />
                    </label>
                    <button
                        type="button"
                        onClick={handleDownload}
                        className="bg-blue-500 text-white rounded p-2 mt-4"
                    >
                        Descargar
                    </button>
                </form>
            </div>
        </Popup>
    );
}

export default DescargarComprobantes;