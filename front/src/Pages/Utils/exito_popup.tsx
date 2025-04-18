import React, { useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useToast,
} from '@chakra-ui/react';

interface ExitoPopupProps {
  open: boolean;
  onClose: () => void;
  texto: string;
}

const ExitoPopup: React.FC<ExitoPopupProps> = ({ open, onClose, texto }) => {
  useEffect(() => {
  }, [open]);

  return (
    <Modal isOpen={open} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader bg="green.100" color="green.800" fontWeight="bold">
          ¡Éxito!
        </ModalHeader>
        <ModalBody textAlign="center" p={6}>
          <p>{texto}</p>
        </ModalBody>
        <ModalFooter>
          <Button colorScheme="green" onClick={onClose}>
            Cerrar
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ExitoPopup;
