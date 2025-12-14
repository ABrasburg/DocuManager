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
  Select,
  useToast,
} from '@chakra-ui/react';
import api from '../../api';

interface Emisor {
  cuit: string;
  denominacion: string;
}

interface Props {
  open: boolean;
  onClose: () => void;
  emisores: Emisor[];
  endpoint: string;
  titulo: string;
  mensajeExito?: string;
  mensajeError?: string;
}

const DescargarComprobantes: React.FC<Props> = ({
  open,
  onClose,
  emisores,
  endpoint,
  titulo,
  mensajeExito = 'Los comprobantes fueron descargados correctamente.',
  mensajeError = 'No se pudieron descargar los comprobantes.'
}) => {
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const [emisorCuit, setEmisorCuit] = useState<string>('');
  const toast = useToast();

  const handleDownload = async () => {
    try {
      const params = new URLSearchParams();

      if (fechaInicio) params.append('fecha_inicio', fechaInicio);
      if (fechaFin) params.append('fecha_fin', fechaFin);
      if (emisorCuit) params.append('emisor_cuit', emisorCuit);

      const response = await api.get(`${endpoint}?${params.toString()}`, {
        responseType: 'blob',
      });

      const disposition = response.headers["content-disposition"];
      let filename = "comprobantes.csv";

      if (disposition && disposition.includes("filename=")) {
        const match = disposition.match(/filename="?([^"]+)"?/);
        if (match?.[1]) {
          filename = match[1];
        }
      }

      const url = window.URL.createObjectURL(response.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      toast({
        title: 'Descarga completada.',
        description: mensajeExito,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

    } catch (error) {
      toast({
        title: 'Error en la descarga.',
        description: mensajeError,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Modal isOpen={open} onClose={onClose} isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>{titulo}</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          <FormControl mb={4}>
            <FormLabel>Emisor</FormLabel>
            <Select
              placeholder="Todos los emisores"
              value={emisorCuit}
              onChange={(e) => setEmisorCuit(e.target.value)}
            >
              {emisores.map((emisor) => (
                <option key={emisor.cuit} value={emisor.cuit}>
                  {emisor.denominacion} - {emisor.cuit}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl mb={4}>
            <FormLabel>Fecha Inicio</FormLabel>
            <Input
              type="date"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
            />
          </FormControl>

          <FormControl>
            <FormLabel>Fecha Fin</FormLabel>
            <Input
              type="date"
              value={fechaFin}
              onChange={(e) => setFechaFin(e.target.value)}
            />
          </FormControl>
        </ModalBody>

        <ModalFooter>
          <Button colorScheme="blue" mr={3} onClick={handleDownload}>
            Descargar
          </Button>
          <Button variant="ghost" onClick={onClose}>Cancelar</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default DescargarComprobantes;
