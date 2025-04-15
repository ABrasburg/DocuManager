import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import React, { useState, useEffect } from 'react';

interface Emisor {
    id: number;
    tipo_doc: string;
    cuit: string;
    denominacion: string;
  }

  interface Props {
    open: boolean;
    onClose: () => void;
    emisor: Emisor;
    editar: boolean;
    nuevo: boolean;
    onCreate: (emisor: Emisor) => void;
    onEdit: (emisor: Emisor) => void;
  }

    const ModificarEmisor: React.FC<Props> = ({ open, onClose, emisor, editar, nuevo, onCreate, onEdit}) => {
        const [tipo_doc, setTipoDoc] = useState<string>("80");
        const [old_cuit, setOldCuit] = useState<string>(emisor.cuit);
        const [cuit, setCuit] = useState<string>(emisor.cuit);
        const [denominacion, setDenominacion] = useState<string>(emisor.denominacion);

    
        const handleEdit = async (event: React.FormEvent) => {
            event.preventDefault();
            try {
                const response = await fetch(`http://localhost:9000/emisor/${old_cuit}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tipo_doc,
                    denominacion,
                    cuit,
                }),
                });
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Success:', data);
                onClose();
            } catch (error) {
                console.error('Error:', error);
            }
        };
        const handleSubmit = async (event: React.FormEvent) => {
            event.preventDefault();
            if (editar) {
                await handleEdit(event);
            } else {
                try {
                    const response = await fetch('http://localhost:9000/emisor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        tipo_doc,
                        cuit,
                        denominacion,
                    }),
                    });
                    if (!response.ok) {
                    throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    console.log('Success:', data);
                    onCreate(data);
                    onClose();
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        };
        useEffect(() => {
            setTipoDoc(tipo_doc);
            setCuit(emisor.cuit);
            setDenominacion(emisor.denominacion);
            setOldCuit(emisor.cuit);
        }, [emisor]);
        return (
            <Popup open={open} onClose={onClose} modal>
                <div className="popup-content">
                    <h2>{editar ? 'Modificar Emisor' : 'Nuevo Emisor'}</h2>
                    <form onSubmit={handleSubmit}>
                        <div>
                            <label>Cuit:</label>
                            <input
                                type="text"
                                value={cuit}
                                onChange={(e) => setCuit(e.target.value)}
                            />
                        </div>
                        <div>
                            <label>Denominacion:</label>
                            <input
                                type="text"
                                value={denominacion}
                                onChange={(e) => setDenominacion(e.target.value)}
                            />
                        </div>
                        <button type="submit">{editar ? 'Modificar' : 'Crear'}</button>
                    </form>
                </div>
            </Popup>
        );
    }
export default ModificarEmisor;