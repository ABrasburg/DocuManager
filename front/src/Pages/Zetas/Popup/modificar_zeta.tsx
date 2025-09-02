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
    gravado: number;
    cuenta_corriente: string;
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
  const [punto_de_venta, setPuntoVenta] = useState<number>(zeta.numero);
  const [numero, setNumero] = useState<number>(zeta.numero);
  const [ultimo_ticket, setUltimoTicket] = useState<number>(zeta.ultimo_ticket);
  const [exento, setExento] = useState<number>(zeta.exento);
  const [iva, setIva] = useState<number>(zeta.iva);
  const [gravado, setGravado] = useState<number>(zeta.gravado);
  const [cuenta_corriente, setCuentaCorriente] = useState<string>(zeta.cuenta_corriente);
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
        gravado,
        cuenta_corriente,
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
    if (!fecha || !punto_de_venta || !numero || !ultimo_ticket || !exento || !iva || !gravado || !cuenta_corriente || !total) {
      toast({
        title: 'Error.',
        description: "Todos los campos son obligatorios.",
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
      return false;
    }
    if (exento < 0) {
      toast({
        title: 'Error.',
        description: "El campo Exento no puede ser negativo.",
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
        gravado,
        cuenta_corriente,
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
      setGravado(zeta.gravado);
      setCuentaCorriente(zeta.cuenta_corriente);
      setTotal(zeta.total);
    } else if (nuevo) {
      setFecha(Date.now());
      setPuntoVenta(0);
      setNumero(0);
      setUltimoTicket(0);
      setExento(0);
      setIva(0);
      setGravado(0);
      setCuentaCorriente('');
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
            <select
              value={numero || ''}
              onChange={(e) => setNumero(Number(e.target.value))}
              style={{
                width: '100%',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc',
              }}
            >
              <option value="" disabled>
                Seleccionar número de Zeta
              </option>
              <option value={8}>8</option>
              <option value={9}>9</option>
            </select>
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
              isReadOnly
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>IVA</FormLabel>
            <Input
              type="number"
              value={iva || ''}
              onChange={(e) => {
              const newIva = e.target.value === '' ? NaN : Number(e.target.value);
              setIva(newIva);
              const newGravado = (newIva / 0.21) + newIva;
              setGravado(parseFloat(newGravado.toFixed(2)));
              const newExento = total - newGravado - Number(cuenta_corriente || 0);
              setExento(parseFloat(newExento.toFixed(2)));
              }}
              onWheel={(e) => e.currentTarget.blur()}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Gravado</FormLabel>
            <Input
              type="number"
              value={gravado || ''}
              isReadOnly
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Cuenta Corriente</FormLabel>
            <Input
              type="text"
              value={cuenta_corriente || ''}
              onChange={(e) => {
              const newCuentaCorriente = e.target.value;
              setCuentaCorriente(newCuentaCorriente);
              const newExento = total - gravado - Number(newCuentaCorriente || 0);
              setExento(parseFloat(newExento.toFixed(2)));
              }}
            />
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Total</FormLabel>
            <Input
              type="number"
              value={total || ''}
              onChange={(e) => {
              const newTotal = e.target.value === '' ? NaN : Number(e.target.value);
              setTotal(newTotal);
              const newExento = newTotal - gravado - Number(cuenta_corriente || 0);
              setExento(parseFloat(newExento.toFixed(2)));
              }}
              onWheel={(e) => e.currentTarget.blur()}
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