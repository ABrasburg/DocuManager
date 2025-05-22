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
  useToast,
} from '@chakra-ui/react';
import api from '../../../api';

interface Props {
  open: boolean;
  onClose: () => void;
}

const DescargarZetas: React.FC<Props> = ({ open, onClose }) => {
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const toast = useToast();

  const handleDownload = async () => {
    try {
      const params = new URLSearchParams({
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });

      const response = await api.get(`/zetas/download?${params.toString()}`, {
        responseType: 'blob',
      });

      const disposition = response.headers["content-disposition"];
      let filename = "zetas.csv";

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
        description: 'Las Zetas fueron descargadas correctamente.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error al descargar.',
        description: 'Hubo un problema al descargar las Zetas.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  return (
    <Modal isOpen={open} onClose={onClose} size="lg">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Descargar Zetas</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <FormControl mb={4}>
            <FormLabel>Fecha Inicio</FormLabel>
            <Input
              type="date"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
            />
          </FormControl>
          <FormControl mb={4}>
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
          <Button variant="ghost" onClick={onClose}>Cerrar</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
export default DescargarZetas;