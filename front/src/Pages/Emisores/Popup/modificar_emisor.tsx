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
      toast({
        title: 'Emisor modificado.',
        description: 'El emisor ha sido modificado correctamente.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      onEdit(data); // Invoca la función onEdit con los nuevos datos
      onClose();
    } catch (error) {
      toast({
        title: 'Error.',
        description: 'Hubo un error al modificar el emisor.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
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
        toast({
          title: 'Emisor creado.',
          description: 'El emisor ha sido creado correctamente.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        onCreate(data); // Invoca la función onCreate con los nuevos datos
        onClose();
      } catch (error) {
        toast({
          title: 'Error.',
          description: 'Hubo un error al crear el emisor.',
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
        console.error('Error:', error);
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
