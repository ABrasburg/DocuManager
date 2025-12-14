import React, { useState, useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  FormControl,
  FormLabel,
  Input,
  Button,
  useToast,
  Divider,
} from '@chakra-ui/react';

import  api from '../../../api';

interface Zeta {
    id: number;
    fecha: number;
    punto_de_venta: number;
    numero: number;
    ultimo_ticket: number;
    exento: number;
    iva: number;
    perfumeria: number;
    medicamentos_iva: number;
    total: number;
}

interface Props {
    open: boolean;
    onClose: () => void;
    zeta: Zeta;
    editar: boolean;
    nuevo: boolean;
    onCreate: (emisor: Zeta) => void;
    onEdit: (emisor: Zeta) => void;
  }
  
const ModificarZeta: React.FC<Props> = ({ open, onClose, zeta, editar, nuevo, onCreate, onEdit }) => {
  const [fecha, setFecha] = useState<number>(zeta.fecha);
  const [punto_de_venta, setPuntoVenta] = useState<number>(zeta.punto_de_venta);
  const [numero, setNumero] = useState<number>(zeta.numero);
  const [ultimo_ticket, setUltimoTicket] = useState<number>(zeta.ultimo_ticket);
  const [exento, setExento] = useState<number>(zeta.exento);
  const [iva, setIva] = useState<number>(zeta.iva);
  const [perfumeria, setPerfumeria] = useState<number>(zeta.perfumeria);
  const [medicamentos_iva, setMedicamentosIva] = useState<number>(zeta.medicamentos_iva);
  const [total, setTotal] = useState<number>(zeta.total);

  const toast = useToast();

  const handleEdit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await api.put(`/zeta/${zeta.id}`, {
        fecha,
        punto_de_venta,
        numero,
        ultimo_ticket,
        exento,
        iva,
        perfumeria,
        medicamentos_iva,
        total,
      });
  
      toast({
        title: 'Zeta modificada.',
        description: "La zeta ha sido modificada.",
        status: 'success',
        duration: 9000,
        isClosable: true,
      });
  
      onEdit(response.data);
    } catch (error) {
      toast({
        title: 'Error.',
        description: "No se pudo modificar la zeta.",
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    } finally {
      onClose();
    }
  };
  
  const validateCreate = () => {
    if (!fecha || !punto_de_venta || !numero || !ultimo_ticket) {
      toast({
        title: 'Error.',
        description: "Todos los campos son obligatorios.",
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
      return false;
    }
    if (exento < 0 || iva < 0) {
      toast({
        title: 'Error.',
        description: "Los campos Exento e IVA no pueden ser negativos.",
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
      return false;
    }
    return true;
  };

  const handleCreate = async (event: React.FormEvent) => {
    if (!validateCreate()) return;
    event.preventDefault();
    try {
      const response = await api.post('/zeta', {
        fecha: new Date(fecha).toISOString().split('T')[0],
        punto_de_venta,
        numero,
        ultimo_ticket,
        exento,
        iva,
        perfumeria,
        medicamentos_iva,
        total,
      });
  
      toast({
        title: 'Zeta creada.',
        description: "La zeta ha sido creada.",
        status: 'success',
        duration: 9000,
        isClosable: true,
      });
      onCreate(response.data);
    } catch (error) {
      toast({
        title: 'Error.',
        description: "No se pudo crear la zeta.",
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    } finally {
      onClose();
    }
  };

  useEffect(() => {
    if (editar) {
      setFecha(zeta.fecha);
      setPuntoVenta(zeta.punto_de_venta);
      setNumero(zeta.numero);
      setUltimoTicket(zeta.ultimo_ticket);
      setExento(zeta.exento);
      setIva(zeta.iva);
      setPerfumeria(zeta.perfumeria);
      setMedicamentosIva(zeta.medicamentos_iva);
      setTotal(zeta.total);
    } else if (nuevo) {
      setFecha(Date.now());
      setPuntoVenta(NaN);
      setNumero(0);
      setUltimoTicket(0);
      setExento(0);
      setIva(0);
      setPerfumeria(0);
      setMedicamentosIva(0);
      setTotal(0);
    }
  }
  , [editar, nuevo, zeta]);

  return (
    <Modal isOpen={open} onClose={onClose} size="lg">
      <ModalOverlay />
      <ModalContent maxHeight="90vh" display="flex" flexDirection="column">
      <ModalHeader>{editar ? 'Modificar Zeta' : 'Crear Zeta'}</ModalHeader>
        <ModalBody overflowY="auto">
          <FormControl isRequired>
            <FormLabel>Fecha</FormLabel>
            <Input
              type="date"
              value={new Date(fecha).toISOString().split('T')[0]}
              onChange={(e) => setFecha(new Date(e.target.value).getTime())}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Punto de venta</FormLabel>
            <Input
              type="number"
              value={punto_de_venta || ''}
              onChange={(e) => setPuntoVenta(e.target.value === '' ? NaN : Number(e.target.value))}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Numero de Zeta</FormLabel>
            <Input
              type="number"
              value={numero || ''}
              onChange={(e) => setNumero(e.target.value === '' ? NaN : Number(e.target.value))}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Último Ticket</FormLabel>
            <Input
              type="number"
              value={ultimo_ticket || ''}
              onChange={(e) => setUltimoTicket(e.target.value === '' ? NaN : Number(e.target.value))}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Exento</FormLabel>
            <Input
              type="number"
              value={exento || ''}
              onChange={(e) => {
                const newExento = e.target.value === '' ? 0 : Number(e.target.value);
                setExento(newExento);
                const newTotal = newExento + iva;
                setTotal(parseFloat(newTotal.toFixed(2)));
              }}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>IVA</FormLabel>
            <Input
              type="number"
              value={iva || ''}
              onChange={(e) => {
                const newIva = e.target.value === '' ? 0 : Number(e.target.value);
                setIva(newIva);
                const newPerfumeria = newIva * 0.20;
                setPerfumeria(parseFloat(newPerfumeria.toFixed(2)));
                const newMedicamentosIva = newIva * 0.80;
                setMedicamentosIva(parseFloat(newMedicamentosIva.toFixed(2)));
                const newTotal = exento + newIva;
                setTotal(parseFloat(newTotal.toFixed(2)));
              }}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Perfumería</FormLabel>
            <Input
              type="number"
              value={perfumeria || ''}
              isReadOnly
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Medicamentos IVA</FormLabel>
            <Input
              type="number"
              value={medicamentos_iva || ''}
              isReadOnly
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Total</FormLabel>
            <Input
              type="number"
              value={total || ''}
              isReadOnly
            />
          </FormControl>
        </ModalBody>
        <Divider />
        <ModalFooter>
          <Button colorScheme="blue" mr={3} onClick={editar ? handleEdit : handleCreate}>
          {editar ? 'Modificar' : 'Crear'}
          </Button>
          <Button variant="ghost" onClick={onClose}>Cancelar</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
export default ModificarZeta;