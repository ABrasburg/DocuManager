import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import React, { useState, useEffect } from 'react';

interface Suma {
    cuit: number;
    fecha_inicio: string;
    fecha_fin: string;
    neto_gravado: number;
    neto_no_gravado: number;
    exento: number;
    otros_tributos: number;
    iva: number;
    total: number;
    }

interface Emisor {
    cuit: string;
    denominacion: string;
}

interface Props {
    open: boolean;
    onClose: () => void;
}

const SumaPopup: React.FC<Props> = ({ open, onClose }) => {
    const [suma, setSuma] = useState<Suma | null>(null);
    const [fechaInicio, setFechaInicio] = useState<string>('');
    const [fechaFin, setFechaFin] = useState<string>('');
    const [cuit, setCuit] = useState<number>(0);
    const [segundoPaso, setSegundoPaso] = useState<boolean>(false);
    const [emisores, setEmisores] = useState<any[]>([]);

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setCuit(Number(e.target.value));
    };
    const handleFechaInicioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFechaInicio(e.target.value);
    };
    const handleFechaFinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFechaFin(e.target.value);
    };
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const data = {
                cuit: cuit,
                fecha_inicio: fechaInicio,
                fecha_fin: fechaFin,
            };
            const queryParams = new URLSearchParams({
                cuit: data.cuit.toString(),
                fecha_inicio: data.fecha_inicio,
                fecha_fin: data.fecha_fin,
            }).toString();

            const response = await fetch(`http://localhost:9000/comprobantes/sumar?${queryParams}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const responseData = await response.json();
            setSuma(responseData);
            setSegundoPaso(true);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };
    const handleClose = () => {
        setSuma(null);
        setCuit(0);
        setFechaInicio('');
        setFechaFin('');
        setSegundoPaso(false);
        onClose();
    };

    const fetchEmisores = async () => {
        try {
            const response = await fetch('http://localhost:9000/emisores');
            const data = await response.json();
            setEmisores(data);
        } catch (error) {
            console.error('Error fetching emisores:', error);
        }
    }

    useEffect(() => {
        console.log('Emisores');
        if (open) {
            fetchEmisores();
        }
    }, [open]);


    return (
        <Popup open={open} onClose={handleClose} modal>
            <div className="popup-content">
                <h2>Obtener Suma</h2>
                {!segundoPaso ? (
                    <form onSubmit={handleSubmit}>
                        <div>
                            <label>
                                Emisor:
                                <select value={cuit} onChange={handleChange} required>
                                    <option value="">Seleccione un emisor</option>
                                    {
                                    emisores.map((emisor: Emisor) => (
                                        <option key={emisor.cuit} value={emisor.cuit}>
                                            {emisor.denominacion}
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>
                        <div>
                            <label>
                                Fecha Inicio:
                                <input type="date" value={fechaInicio} onChange={handleFechaInicioChange} required />
                            </label>
                        </div>
                        <div>
                            <label>
                                Fecha Fin:
                                <input type="date" value={fechaFin} onChange={handleFechaFinChange} required />
                            </label>
                        </div>
                        <div>
                            <button type="submit">Consultar</button>
                        </div>
                    </form>
                ) : (
                    <div>
                        {suma && (
                            <>
                                <h3>Resultados:</h3>
                                <p>Cuit: {suma.cuit}</p>
                                <p>Fecha Inicio: {suma.fecha_inicio}</p>
                                <p>Fecha Fin: {suma.fecha_fin}</p>
                                <p>Neto Gravado: {suma.neto_gravado}</p>
                                <p>Neto No Gravado: {suma.neto_no_gravado}</p>
                                <p>Exento: {suma.exento}</p>
                                <p>Otros Tributos: {suma.otros_tributos}</p>
                                <p>IVA: {suma.iva}</p>
                                <p>Total: {suma.total}</p>
                            </>
                        )}
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <button onClick={() => setSegundoPaso(false)}>Atrás</button>
                            <button onClick={handleClose}>Cerrar</button>
                        </div>
                    </div>
                )}
            </div>
        </Popup>
    );
}

export default SumaPopup;
