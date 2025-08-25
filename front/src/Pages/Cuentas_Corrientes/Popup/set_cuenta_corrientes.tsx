import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Checkbox,
  Grid,
  GridItem,
  Text,
  useToast,
} from '@chakra-ui/react';
import React from 'react';
import api from '../../../api';

interface Emisor {
  cuit: string;
  denominacion: string;
  cuenta_corriente: boolean;
}

interface SetCuentaCorrienteProps {
  isOpen: boolean;
  onClose: () => void;
  emisores: Emisor[];
  onSetCuentaCorriente: (cuit: string, cuentaCorriente: boolean) => void;
}

const SetCuentaCorriente: React.FC<SetCuentaCorrienteProps> = ({
  isOpen,
  onClose,
  emisores,
  onSetCuentaCorriente,
}) => {
  const toast = useToast();

  const handleCheckboxChange = async (cuit: string, checked: boolean) => {
    try {
      await api.put(`/emisor/${cuit}/cuenta_corriente?cuenta_corriente=${checked}`);
      onSetCuentaCorriente(cuit, checked);
      toast({
        title: 'Éxito',
        description: `Cuenta corriente ${checked ? 'activada' : 'desactivada'} para el emisor`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'No se pudo actualizar la cuenta corriente',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="lg">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Cuales tienen Cuenta Corriente</ModalHeader>
        <ModalCloseButton />
        <ModalBody maxHeight="400px" overflowY="auto">
          <Grid templateColumns="1fr auto" gap={2}>
            {emisores.map((emisor) => (
              <React.Fragment key={emisor.cuit}>
                <GridItem>
                  <Text>{emisor.denominacion}</Text>
                </GridItem>
                <GridItem>
                  <Checkbox
                    isChecked={emisor.cuenta_corriente}
                    onChange={(e) =>
                      handleCheckboxChange(emisor.cuit, e.target.checked)
                    }
                  />
                </GridItem>
              </React.Fragment>
            ))}
          </Grid>
        </ModalBody>
        <ModalFooter>
          <Button onClick={onClose} mr={3}>Cerrar</Button>
          <Button colorScheme="blue" onClick={onClose}>Guardar</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default SetCuentaCorriente;
