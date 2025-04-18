import React from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  ModalFooter,
  Button,
  Text,
  Stack,
} from '@chakra-ui/react';

interface Comprobante {
  id: number;
  fecha_emision: string;
  punto_venta: number;
  numero_desde: number;
  numero_hasta: number;
  cod_autorizacion: string;
  tipo_cambio: number;
  moneda: string;
  total: number;
  emisor: {
    cuit: string;
    denominacion: string;
  };
  tipo_comprobante: {
    nombre: string;
  };
}

interface Props {
  open: boolean;
  comprobante: Comprobante | null;
  onClose: () => void;
}

const ComprobantePopup: React.FC<Props> = ({ comprobante, onClose, open }) => {
  return (
    <Modal isOpen={open} onClose={onClose} size="lg" isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Detalle del Comprobante</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {comprobante ? (
            <Stack spacing={3}>
              <Text><strong>Fecha emisión:</strong> {comprobante.fecha_emision}</Text>
              <Text><strong>Punto de venta:</strong> {comprobante.punto_venta}</Text>
              <Text><strong>Número desde:</strong> {comprobante.numero_desde}</Text>
              <Text><strong>Número hasta:</strong> {comprobante.numero_hasta}</Text>
              <Text><strong>Cod. autorización:</strong> {comprobante.cod_autorizacion}</Text>
              <Text><strong>Tipo cambio:</strong> {comprobante.tipo_cambio}</Text>
              <Text><strong>Moneda:</strong> {comprobante.moneda}</Text>
              <Text><strong>Total:</strong> ${comprobante.total}</Text>
              <Text><strong>Emisor:</strong> {comprobante.emisor.denominacion} ({comprobante.emisor.cuit})</Text>
              <Text><strong>Tipo de comprobante:</strong> {comprobante.tipo_comprobante.nombre}</Text>
            </Stack>
          ) : (
            <Text>No hay datos disponibles para este comprobante.</Text>
          )}
        </ModalBody>

        <ModalFooter>
          <Button onClick={onClose} colorScheme="blue">
            Cerrar
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ComprobantePopup;
