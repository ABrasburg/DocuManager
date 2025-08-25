import React, { useState } from 'react';
import { Modal, Form, Input, DatePicker, Button, message } from 'antd';
import dayjs from 'dayjs';
import api from '../../../api';

interface MarcarPagadoProps {
  visible: boolean;
  onClose: () => void;
  comprobante: {
    id: number;
    fecha_emision: string;
    numero_desde: number;
    numero_hasta: number;
    emisor: {
      denominacion: string;
    };
  } | null;
  onSuccess: () => void;
}

const MarcarPagado: React.FC<MarcarPagadoProps> = ({
  visible,
  onClose,
  comprobante,
  onSuccess,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: any) => {
    if (!comprobante) return;
    
    setLoading(true);
    try {
      await api.put(`/comprobante/${comprobante.id}/marcar_pagado`, {
        fecha_pago: values.fecha_pago.format('YYYY-MM-DD'),
        numero_ticket: values.numero_ticket,
      });
      
      message.success('Comprobante marcado como pagado exitosamente');
      onSuccess();
      onClose();
      form.resetFields();
    } catch (error) {
      message.error('Error al marcar el comprobante como pagado');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title="Marcar Comprobante como Pagado"
      open={visible}
      onCancel={handleCancel}
      footer={null}
      width={500}
    >
      {comprobante && (
        <>
          <div style={{ marginBottom: 16, padding: 12, backgroundColor: '#f5f5f5', borderRadius: 6 }}>
            <p><strong>Emisor:</strong> {comprobante.emisor.denominacion}</p>
            <p><strong>Comprobante:</strong> {comprobante.numero_desde} - {comprobante.numero_hasta}</p>
            <p><strong>Fecha Emisión:</strong> {comprobante.fecha_emision}</p>
          </div>

          <Form
            form={form}
            layout="vertical"
            onFinish={handleSubmit}
          >
            <Form.Item
              name="fecha_pago"
              label="Fecha de Pago"
              rules={[{ required: true, message: 'Por favor seleccione la fecha de pago' }]}
            >
              <DatePicker 
                style={{ width: '100%' }}
                format="YYYY-MM-DD"
                placeholder="Seleccionar fecha de pago"
              />
            </Form.Item>

            <Form.Item
              name="numero_ticket"
              label="Número de Ticket"
              rules={[{ required: true, message: 'Por favor ingrese el número de ticket' }]}
            >
              <Input 
                placeholder="Ej: TK-001234"
                maxLength={50}
              />
            </Form.Item>

            <div style={{ textAlign: 'right', marginTop: 16 }}>
              <Button onClick={handleCancel} style={{ marginRight: 8 }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" loading={loading}>
                Marcar como Pagado
              </Button>
            </div>
          </Form>
        </>
      )}
    </Modal>
  );
};

export default MarcarPagado;