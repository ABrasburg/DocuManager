import React, { useState } from 'react';
import { Modal, Form, Input, DatePicker, Button, message, List } from 'antd';
import api from '../../../api';

interface Comprobante {
  id: number;
  fecha_emision: string;
  numero_desde: number;
  numero_hasta: number;
  emisor: {
    denominacion: string;
  };
}

interface MarcarPagadoProps {
  visible: boolean;
  onClose: () => void;
  comprobante: Comprobante | null;
  comprobantes: Comprobante[];
  onSuccess: () => void;
}

const MarcarPagado: React.FC<MarcarPagadoProps> = ({
  visible,
  onClose,
  comprobante,
  comprobantes,
  onSuccess,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const isMultiple = comprobantes.length > 1;
  const displayComprobantes = isMultiple ? comprobantes : (comprobante ? [comprobante] : []);

  const handleSubmit = async (values: any) => {
    if (displayComprobantes.length === 0) return;

    setLoading(true);
    try {
      const fecha_pago = values.fecha_pago.format('YYYY-MM-DD');
      const numero_ticket = values.numero_ticket;

      // Procesar todos los comprobantes en paralelo
      await Promise.all(
        displayComprobantes.map(comp =>
          api.put(`/comprobante/${comp.id}/marcar_pagado`, {
            fecha_pago,
            numero_ticket,
          })
        )
      );

      message.success(`${displayComprobantes.length} comprobante(s) marcado(s) como pagado exitosamente`);
      onSuccess();
      onClose();
      form.resetFields();
    } catch (error) {
      message.error('Error al marcar los comprobantes como pagados');
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
      title={isMultiple ? `Marcar ${displayComprobantes.length} Comprobantes como Pagados` : "Marcar Comprobante como Pagado"}
      open={visible}
      onCancel={handleCancel}
      footer={null}
      width={600}
    >
      {displayComprobantes.length > 0 && (
        <>
          <div style={{ marginBottom: 16, padding: 12, backgroundColor: '#f5f5f5', borderRadius: 6, maxHeight: '200px', overflowY: 'auto' }}>
            {isMultiple ? (
              <>
                <p style={{ marginBottom: 8, fontWeight: 'bold' }}>Comprobantes seleccionados:</p>
                <List
                  size="small"
                  dataSource={displayComprobantes}
                  renderItem={(comp) => (
                    <List.Item>
                      <div>
                        <strong>{comp.emisor.denominacion}</strong> - Comprobante: {comp.numero_desde} - {comp.numero_hasta} (Fecha: {comp.fecha_emision})
                      </div>
                    </List.Item>
                  )}
                />
              </>
            ) : (
              <>
                <p><strong>Emisor:</strong> {displayComprobantes[0].emisor.denominacion}</p>
                <p><strong>Comprobante:</strong> {displayComprobantes[0].numero_desde} - {displayComprobantes[0].numero_hasta}</p>
                <p><strong>Fecha Emisión:</strong> {displayComprobantes[0].fecha_emision}</p>
              </>
            )}
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