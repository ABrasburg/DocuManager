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

const DescargarComprobantes: React.FC<Props> = ({ open, onClose }) => {
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const toast = useToast();

  const handleDownload = async () => {
    try {
      const params = new URLSearchParams({
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });
  
      const response = await api.get(`/comprobantes/download?${params.toString()}`, {
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
        description: 'Los comprobantes fueron descargados correctamente.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
  
    } catch (error) {
      toast({
        title: 'Error en la descarga.',
        description: 'No se pudieron descargar los comprobantes.',
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
        <ModalHeader>Descargar Comprobantes</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
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
