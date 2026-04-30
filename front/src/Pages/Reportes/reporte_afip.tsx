import React, { useState } from 'react';
import { DatePicker, Button, Card, Space, Typography, Spin, message } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '../../api';
import Navbar from '../Utils/navbar';
import ErrorPopup from '../Utils/error_popup';
import { formatNumber } from '../../Utils/formatNumber';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;

interface ReporteData {
  periodo: {
    fecha_inicio: string;
    fecha_fin: string;
    cantidad_dias: number;
  };
  exento: number;
  gravado: number;
  perfumeria: number;
  medicamentos_iva: number;
  iva: number;
  total: number;
}

const ReporteAFIP: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [reporteData, setReporteData] = useState<ReporteData | null>(null);
  const [fechaInicio, setFechaInicio] = useState<string>('');
  const [fechaFin, setFechaFin] = useState<string>('');
  const [showErrorPopup, setShowErrorPopup] = useState(false);
  const [textoError, setTextoError] = useState('');

  const handleDateChange = (dates: any) => {
    if (dates && dates.length === 2) {
      setFechaInicio(dates[0].format('YYYY-MM-DD'));
      setFechaFin(dates[1].format('YYYY-MM-DD'));
    } else {
      setFechaInicio('');
      setFechaFin('');
    }
  };

  const generarReporte = async () => {
    if (!fechaInicio || !fechaFin) {
      message.error('Debe seleccionar un rango de fechas');
      return;
    }

    setLoading(true);
    try {
      const response = await api.get(`/comprobantes/reporte_afip`, {
        params: {
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin,
        },
      });
      setReporteData(response.data);
    } catch (error: any) {
      console.error('Error al generar reporte:', error);
      setTextoError(error.response?.data?.detail || 'Error al generar el reporte');
      setShowErrorPopup(true);
    }
    setLoading(false);
  };

  return (
    <div>
      <Navbar />
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: '30px' }}>
          Informe General de Comprobantes
        </Title>

        <Card style={{ marginBottom: '20px' }}>
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <div style={{ textAlign: 'center' }}>
              <Text strong>Seleccionar período:</Text>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '15px' }}>
              <Text>Desde:</Text>
              <RangePicker
                format="DD/MM/YYYY"
                onChange={handleDateChange}
                placeholder={['Fecha inicio', 'Fecha fin']}
              />
              <Button 
                type="primary" 
                icon={<SearchOutlined />}
                onClick={generarReporte}
                loading={loading}
              >
                Buscar
              </Button>
            </div>
          </Space>
        </Card>

        {loading && (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <div style={{ marginTop: '10px' }}>Generando reporte...</div>
          </div>
        )}

        {reporteData && !loading && (
          <Card>
            <div style={{ border: '2px solid #d4a574', borderRadius: '8px', padding: '20px', backgroundColor: '#faf8f5' }}>

              <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <Title level={4} style={{ margin: 0, color: '#8b5a2b' }}>
                  Informe general de comprobantes
                </Title>
                <Text>
                  Desde: {dayjs(reporteData.periodo.fecha_inicio).format('DD/MM/YYYY')}
                  {' - '}
                  Hasta: {dayjs(reporteData.periodo.fecha_fin).format('DD/MM/YYYY')}
                  {' · '}
                  {reporteData.periodo.cantidad_dias} días
                </Text>
              </div>

              <div style={{ backgroundColor: '#fff', padding: '15px', borderRadius: '6px', border: '1px solid #d9d9d9' }}>
                <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text>Exento:</Text>
                  <Text strong>{formatNumber(reporteData.exento)}</Text>
                </div>
                <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text>Gravado:</Text>
                  <Text strong>{formatNumber(reporteData.gravado)}</Text>
                </div>
                <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text>Perfumería:</Text>
                  <Text strong>{formatNumber(reporteData.perfumeria)}</Text>
                </div>
                <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text>Medicamentos IVA:</Text>
                  <Text strong>{formatNumber(reporteData.medicamentos_iva)}</Text>
                </div>
                <div style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text>IVA:</Text>
                  <Text strong>{formatNumber(reporteData.iva)}</Text>
                </div>
                <div style={{ borderTop: '1px solid #d9d9d9', paddingTop: '10px', marginTop: '10px', display: 'flex', justifyContent: 'space-between' }}>
                  <Text strong style={{ fontSize: '16px' }}>Total:</Text>
                  <Text strong style={{ fontSize: '16px' }}>{formatNumber(reporteData.total)}</Text>
                </div>
              </div>

            </div>
          </Card>
        )}

        {showErrorPopup && (
          <ErrorPopup
            open={showErrorPopup}
            texto={textoError}
            onClose={() => setShowErrorPopup(false)}
          />
        )}
      </div>
    </div>
  );
};

export default ReporteAFIP;