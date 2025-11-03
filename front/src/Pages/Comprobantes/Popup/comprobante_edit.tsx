import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  FormControl,
  FormLabel,
  Grid,
  Text,
} from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';

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
  onClose: () => void;
  comprobante: Comprobante | null;
  handleSave: (comprobante: Comprobante) => void;
}

const ComprobantePopup: React.FC<Props> = ({ comprobante, onClose, open, handleSave }) => {
  const [editableComprobante, setEditableComprobante] = useState<Comprobante | null>(null);

  useEffect(() => {
    if (comprobante) {
      setEditableComprobante(comprobante);
    }
  }, [comprobante]);

  const handleChange = <K extends keyof Comprobante>(field: K, value: Comprobante[K]) => {
    if (editableComprobante) {
      setEditableComprobante({
        ...editableComprobante,
        [field]: value,
      });
    }
  };

  const handleEmisorChange = (field: keyof Comprobante['emisor'], value: string) => {
    if (editableComprobante) {
      setEditableComprobante({
        ...editableComprobante,
        emisor: {
          ...editableComprobante.emisor,
          [field]: value,
        },
      });
    }
  };

  const handleTipoComprobanteChange = (value: string) => {
    if (editableComprobante) {
      setEditableComprobante({
        ...editableComprobante,
        tipo_comprobante: {
          ...editableComprobante.tipo_comprobante,
          nombre: value,
        },
      });
    }
  };

  const isValidDate = (dateString: string) => {
    // Validar formato YYYY-MM-DD
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateString)) return false;

    // Validar que sea una fecha válida
    const date = new Date(dateString);
    return !isNaN(date.getTime());
  };

  const isValid =
    editableComprobante &&
    editableComprobante.fecha_emision !== null &&
    editableComprobante.fecha_emision !== undefined &&
    String(editableComprobante.fecha_emision).trim() !== '' &&
    isValidDate(String(editableComprobante.fecha_emision)) &&
    editableComprobante.cod_autorizacion !== null &&
    editableComprobante.cod_autorizacion !== undefined &&
    String(editableComprobante.cod_autorizacion).trim() !== '' &&
    editableComprobante.total >= 0;

  return (
    <Modal isOpen={open} onClose={onClose} size="xl" isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Editar Comprobante</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {editableComprobante ? (
            <>
              <FormControl mb={4}>
                <FormLabel>Fecha emisión</FormLabel>
                <Input
                  type="text"
                  value={editableComprobante.fecha_emision}
                  onChange={(e) => handleChange('fecha_emision', e.target.value)}
                  autoFocus
                />
              </FormControl>

              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <FormControl>
                  <FormLabel>Punto de venta</FormLabel>
                  <Input
                    type="number"
                    value={editableComprobante.punto_venta}
                    onChange={(e) => handleChange('punto_venta', Number(e.target.value))}
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Tipo cambio</FormLabel>
                  <Input
                    type="number"
                    value={editableComprobante.tipo_cambio}
                    onChange={(e) => handleChange('tipo_cambio', Number(e.target.value))}
                  />
                </FormControl>
              </Grid>

              <Grid templateColumns="repeat(2, 1fr)" gap={4} mt={4}>
                <FormControl>
                  <FormLabel>Número desde</FormLabel>
                  <Input
                    type="number"
                    value={editableComprobante.numero_desde}
                    onChange={(e) => handleChange('numero_desde', Number(e.target.value))}
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Número hasta</FormLabel>
                  <Input
                    type="number"
                    value={editableComprobante.numero_hasta}
                    onChange={(e) => handleChange('numero_hasta', Number(e.target.value))}
                  />
                </FormControl>
              </Grid>

              <FormControl mt={4}>
                <FormLabel>Cod. autorización</FormLabel>
                <Input
                  type="text"
                  value={editableComprobante.cod_autorizacion}
                  onChange={(e) => handleChange('cod_autorizacion', e.target.value)}
                />
              </FormControl>

              <FormControl mt={4}>
                <FormLabel>Moneda</FormLabel>
                <Input
                  type="text"
                  value={editableComprobante.moneda}
                  onChange={(e) => handleChange('moneda', e.target.value)}
                />
              </FormControl>

              <FormControl mt={4}>
                <FormLabel>Total</FormLabel>
                <Input
                  type="number"
                  value={editableComprobante.total}
                  onChange={(e) => handleChange('total', Number(e.target.value))}
                />
              </FormControl>

              <FormControl mt={4}>
                <FormLabel>Emisor</FormLabel>
                <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                  <Input
                    placeholder="Denominación"
                    value={editableComprobante.emisor.denominacion}
                    onChange={(e) => handleEmisorChange('denominacion', e.target.value)}
                  />
                  <Input
                    placeholder="CUIT"
                    value={editableComprobante.emisor.cuit}
                    onChange={(e) => handleEmisorChange('cuit', e.target.value)}
                  />
                </Grid>
              </FormControl>

              <FormControl mt={4}>
                <FormLabel>Tipo de comprobante</FormLabel>
                <Input
                  type="text"
                  value={editableComprobante.tipo_comprobante.nombre}
                  onChange={(e) => handleTipoComprobanteChange(e.target.value)}
                />
              </FormControl>
            </>
          ) : (
            <Text color="red.500">No hay datos disponibles para este comprobante.</Text>
          )}
        </ModalBody>

        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cerrar
          </Button>
          <Button
            colorScheme="blue"
            onClick={() => {
              if (editableComprobante) {
                handleSave(editableComprobante);
              }
              onClose();
            }}
            isDisabled={!isValid}
          >
            Guardar
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ComprobantePopup;
