import React, { useState, useEffect } from 'react';
import { Modal, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton, Button, FormControl, FormLabel, Select, Input } from '@chakra-ui/react';

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

    const fetchEmisores = async () => {
        try {
            const response = await fetch('http://localhost:9000/emisores');
            const data = await response.json();
            setEmisores(data);
        } catch (error) {
            console.error('Error fetching emisores:', error);
        }
    };

    useEffect(() => {
        if (open) {
            fetchEmisores();
        }
    }, [open]);

    return (
        <Modal isOpen={open} onClose={onClose} isCentered>
            <ModalContent>
                <ModalCloseButton />
                <ModalHeader>Obtener Suma</ModalHeader>
                <ModalBody>
                    {!segundoPaso ? (
                        <form onSubmit={handleSubmit}>
                            <FormControl mb={4}>
                                <FormLabel>Emisor</FormLabel>
                                <Select value={cuit} onChange={handleChange} required>
                                    <option value="">Seleccione un emisor</option>
                                    {emisores.map((emisor: Emisor) => (
                                        <option key={emisor.cuit} value={emisor.cuit}>
                                            {emisor.denominacion}
                                        </option>
                                    ))}
                                </Select>
                            </FormControl>
                            <FormControl mb={4}>
                                <FormLabel>Fecha Inicio</FormLabel>
                                <Input type="date" value={fechaInicio} onChange={handleFechaInicioChange} required />
                            </FormControl>
                            <FormControl mb={4}>
                                <FormLabel>Fecha Fin</FormLabel>
                                <Input type="date" value={fechaFin} onChange={handleFechaFinChange} required />
                            </FormControl>
                            <Button type="submit" colorScheme="blue" width="full">
                                Consultar
                            </Button>
                        </form>
                    ) : (
                        <>
                            {suma && (
                                <div>
                                    <h3>Resultados:</h3>
                                    <p>Cuit: {suma.cuit}</p>
                                    <p>Fecha Inicio: {suma.fecha_inicio}</p>
                                    <p>Fecha Fin: {suma.fecha_fin}</p>
                                    <p>Neto Gravado: {suma.neto_gravado.toFixed(2)}</p>
                                    <p>Neto No Gravado: {suma.neto_no_gravado.toFixed(2)}</p>
                                    <p>Exento: {suma.exento.toFixed(2)}</p>
                                    <p>Otros Tributos: {suma.otros_tributos.toFixed(2)}</p>
                                    <p>IVA: {suma.iva.toFixed(2)}</p>
                                    <p>Total: {suma.total.toFixed(2)}</p>
                                </div>
                            )}
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <Button onClick={() => setSegundoPaso(false)} colorScheme="gray">
                                    Atrás
                                </Button>
                                <Button onClick={onClose} colorScheme="red">
                                    Cerrar
                                </Button>
                            </div>
                        </>
                    )}
                </ModalBody>
                <ModalFooter />
            </ModalContent>
        </Modal>
    );
};

export default SumaPopup;