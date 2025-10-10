import React, { useState, useEffect } from 'react';
import { Modal, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton, Button, FormControl, FormLabel, Select, Input } from '@chakra-ui/react';
import api from '../../../api';
import { formatCurrency } from '../../../Utils/formatNumber';

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
      
          const response = await api.get(`/comprobantes/sumar?${queryParams}`, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
      
          setSuma(response.data);
          setSegundoPaso(true);
        } catch (error) {
        }
      };      

      const fetchEmisores = async () => {
        try {
          const response = await api.get('/emisores');
          setEmisores(response.data);
        } catch (error) {
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
                                    <h3 style={{ fontWeight: 'bold', marginBottom: '10px' }}>Resultados:</h3>
                                    <p><strong>Cuit:</strong> {suma.cuit}</p>
                                    <p><strong>Fecha Inicio:</strong> {suma.fecha_inicio}</p>
                                    <p><strong>Fecha Fin:</strong> {suma.fecha_fin}</p>
                                    <p><strong>Neto Gravado:</strong> {formatCurrency(suma.neto_gravado)}</p>
                                    <p><strong>Neto No Gravado:</strong> {formatCurrency(suma.neto_no_gravado)}</p>
                                    <p><strong>Exento:</strong> {formatCurrency(suma.exento)}</p>
                                    <p><strong>Otros Tributos:</strong> {formatCurrency(suma.otros_tributos)}</p>
                                    <p><strong>IVA:</strong> {formatCurrency(suma.iva)}</p>
                                    <p style={{ fontSize: '18px', fontWeight: 'bold', marginTop: '10px' }}><strong>Total:</strong> {formatCurrency(suma.total)}</p>
                                </div>
                            )}
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
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