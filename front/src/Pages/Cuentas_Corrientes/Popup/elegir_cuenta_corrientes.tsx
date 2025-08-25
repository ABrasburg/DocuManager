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

interface Emisor {
    cuit: string;
    denominacion: string;
    cuenta_corriente: boolean;
  }

interface Props {
  open: boolean;
  onClose: () => void;
  emisores: Emisor[];
  handleChange: (cuit: string, cuenta_corriente: boolean) => void;
}