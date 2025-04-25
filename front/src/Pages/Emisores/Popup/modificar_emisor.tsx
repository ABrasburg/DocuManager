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
} from '@chakra-ui/react';

import api from '../../../api';

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

const ModificarEmisor: React.FC<Props> = ({ open, onClose, emisor, editar, nuevo, onCreate, onEdit }) => {
  const [tipo_doc, setTipoDoc] = useState<string>('80');
  const [old_cuit, setOldCuit] = useState<string>(emisor.cuit);
  const [cuit, setCuit] = useState<string>(emisor.cuit);
  const [denominacion, setDenominacion] = useState<string>(emisor.denominacion);

  const toast = useToast();

  const handleEdit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await api.put(`/emisor/${old_cuit}`, {
        tipo_doc,
        denominacion,
        cuit,
      });
  
      toast({
        title: 'Emisor modificado.',
        description: 'El emisor ha sido modificado correctamente.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
  
      onEdit(response.data);
      onClose();
    } catch (error) {
      toast({
        title: 'Error.',
        description: 'Hubo un error al modificar el emisor.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };  

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (editar) {
      await handleEdit(event);
    } else {
      try {
        const response = await api.post('/emisor', {
          tipo_doc,
          cuit,
          denominacion,
        });
  
        toast({
          title: 'Emisor creado.',
          description: 'El emisor ha sido creado correctamente.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
  
        onCreate(response.data);
        onClose();
      } catch (error) {
        toast({
          title: 'Error.',
          description: 'Hubo un error al crear el emisor.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      }
    }
  };  

  useEffect(() => {
    setTipoDoc(emisor.tipo_doc);
    setCuit(emisor.cuit);
    setDenominacion(emisor.denominacion);
    setOldCuit(emisor.cuit);
  }, [emisor]);

  return (
    <Modal isOpen={open} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>{editar ? 'Modificar Emisor' : 'Nuevo Emisor'}</ModalHeader>
        <ModalBody>
          <form onSubmit={handleSubmit}>
            <FormControl id="cuit" mb={4}>
              <FormLabel>CUIT</FormLabel>
              <Input
                type="text"
                value={cuit}
                onChange={(e) => setCuit(e.target.value)}
                placeholder="CUIT"
              />
            </FormControl>
            <FormControl id="denominacion" mb={4}>
              <FormLabel>Denominación</FormLabel>
              <Input
                type="text"
                value={denominacion}
                onChange={(e) => setDenominacion(e.target.value)}
                placeholder="Denominación"
              />
            </FormControl>
          </form>
        </ModalBody>
        <ModalFooter>
          <Button variant="ghost" onClick={onClose} mr={3}>
            Cancelar
          </Button>
          <Button colorScheme="blue" onClick={handleSubmit}>
            {editar ? 'Modificar' : 'Crear'}
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ModificarEmisor;
