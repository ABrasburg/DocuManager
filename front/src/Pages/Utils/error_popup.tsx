import React, { useEffect } from 'react';
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Button,
} from '@chakra-ui/react';

interface ErrorPopupProps {
    open: boolean;
    onClose: () => void;
    texto: string;
}

const ErrorPopup: React.FC<ErrorPopupProps> = ({ open, onClose, texto }) => {
    useEffect(() => {}, [open]);

    return (
        <Modal isOpen={open} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader bg="red.100" color="red.800" fontWeight="bold">
                    ¡Error!
                </ModalHeader>
                <ModalBody textAlign="center" p={6}>
                    <p>{texto}</p>
                </ModalBody>
                <ModalFooter>
                    <Button colorScheme="red" onClick={onClose}>
                        Cerrar
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default ErrorPopup;