import React, { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  FormControl,
  FormLabel,
  Input,
  Alert,
  AlertIcon,
  AlertDescription,
  Text,
  useToast,
} from '@chakra-ui/react';
import api from '../../../api';

interface Props {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const BorrarPorFechas: React.FC<Props> = ({ open, onClose, onSuccess }) => {
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const [confirmando, setConfirmando] = useState(false);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleCerrar = () => {
    setFechaInicio('');
    setFechaFin('');
    setConfirmando(false);
    onClose();
  };

  const handleContinuar = () => {
    if (!fechaInicio || !fechaFin) {
      toast({ title: 'Completá ambas fechas.', status: 'warning', duration: 3000, isClosable: true });
      return;
    }
    if (fechaInicio > fechaFin) {
      toast({ title: 'La fecha de inicio debe ser anterior o igual a la fecha fin.', status: 'warning', duration: 3000, isClosable: true });
      return;
    }
    setConfirmando(true);
  };

  const handleBorrar = async () => {
    setLoading(true);
    try {
      const response = await api.delete('/comprobantes/por_fechas', {
        params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
      });
      const eliminados = response.data.eliminados;
      toast({
        title: `${eliminados} comprobante${eliminados !== 1 ? 's' : ''} eliminado${eliminados !== 1 ? 's' : ''}.`,
        status: 'success',
        duration: 4000,
        isClosable: true,
      });
      onSuccess();
      handleCerrar();
    } catch (error: any) {
      toast({
        title: 'Error al eliminar.',
        description: error.response?.data?.detail || 'Error desconocido.',
        status: 'error',
        duration: 4000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const formatFecha = (f: string) => {
    if (!f) return '';
    const [y, m, d] = f.split('-');
    return `${d}/${m}/${y}`;
  };

  return (
    <Modal isOpen={open} onClose={handleCerrar} isCentered>
      <ModalOverlay />
      <ModalContent>
        {!confirmando ? (
          <>
            <ModalHeader>Borrar comprobantes por rango de fechas</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <Alert status="warning" borderRadius="md" mb={4}>
                <AlertIcon />
                <AlertDescription fontSize="sm">
                  Esta acción eliminará de forma permanente todos los comprobantes de la farmacia seleccionada dentro del rango indicado. No se puede deshacer.
                </AlertDescription>
              </Alert>
              <FormControl mb={4}>
                <FormLabel>Fecha inicio (inclusive)</FormLabel>
                <Input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} />
              </FormControl>
              <FormControl>
                <FormLabel>Fecha fin (inclusive)</FormLabel>
                <Input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} />
              </FormControl>
            </ModalBody>
            <ModalFooter>
              <Button colorScheme="red" mr={3} onClick={handleContinuar}>
                Continuar
              </Button>
              <Button variant="ghost" onClick={handleCerrar}>Cancelar</Button>
            </ModalFooter>
          </>
        ) : (
          <>
            <ModalHeader>Confirmar borrado</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <Alert status="error" borderRadius="md" mb={4}>
                <AlertIcon />
                <AlertDescription fontSize="sm">
                  ¿Confirmás que querés eliminar <strong>todos los comprobantes</strong> de la farmacia actual entre el <strong>{formatFecha(fechaInicio)}</strong> y el <strong>{formatFecha(fechaFin)}</strong> inclusive? Esta acción no se puede deshacer.
                </AlertDescription>
              </Alert>
              <Text fontSize="sm" color="gray.600">
                Solo se borrarán los comprobantes de la farmacia seleccionada actualmente.
              </Text>
            </ModalBody>
            <ModalFooter>
              <Button colorScheme="red" mr={3} onClick={handleBorrar} isLoading={loading}>
                Sí, borrar
              </Button>
              <Button variant="ghost" onClick={() => setConfirmando(false)}>Volver</Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  );
};

export default BorrarPorFechas;
