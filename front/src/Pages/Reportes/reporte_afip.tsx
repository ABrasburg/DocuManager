import React, { useState } from 'react';
import { DatePicker, Button, Card, Space, Typography, Row, Col, Spin, message } from 'antd';
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
  compras: {
    subtotal_exento: number;
    subtotal_gravado: number;
    iva: number;
    subtotal: number;
  };
  ventas: {
    exento: number;
    gravado: number;
    total: number;
  };
  diferencia: {
    cantidad_dias: number;
    gravado: number;
    total: number;
  };
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
                </Text>
              </div>

              <Row gutter={[16, 16]}>
                <Col xs={24} md={11}>
                  <div style={{ backgroundColor: '#fff', padding: '15px', borderRadius: '6px', border: '1px solid #d9d9d9' }}>
                    <Title level={5} style={{ margin: '0 0 15px 0', color: '#8b4513' }}>COMPRAS</Title>
                    
                    <div style={{ marginBottom: '8px' }}>
                      <Text>Subtotal Exento:</Text>
                      <Text strong style={{ float: 'right' }}>{formatNumber(reporteData.compras.subtotal_exento)}</Text>
                    </div>
                    
                    <div style={{ marginBottom: '8px' }}>
                      <Text>Subtotal Gravado:</Text>
                      <Text strong style={{ float: 'right' }}>{formatNumber(reporteData.compras.subtotal_gravado)}</Text>
                    </div>
                    
                    <div style={{ marginBottom: '8px' }}>
                      <Text>IVA:</Text>
                      <Text strong style={{ float: 'right' }}>{formatNumber(reporteData.compras.iva)}</Text>
                    </div>
                    
                    <div style={{ borderTop: '1px solid #d9d9d9', paddingTop: '8px', marginTop: '8px' }}>
                      <Text strong>Subtotal:</Text>
                      <Text strong style={{ float: 'right', fontSize: '16px' }}>{formatNumber(reporteData.compras.subtotal)}</Text>
                    </div>
                  </div>
                </Col>

                <Col xs={24} md={11} offset={1}>
                  <div style={{ backgroundColor: '#fff', padding: '15px', borderRadius: '6px', border: '1px solid #d9d9d9' }}>
                    <Title level={5} style={{ margin: '0 0 15px 0', color: '#6b5b47' }}>VENTAS</Title>
                    
                    <div style={{ marginBottom: '8px' }}>
                      <Text>Exento:</Text>
                      <Text strong style={{ float: 'right' }}>{formatNumber(reporteData.ventas.exento)}</Text>
                    </div>
                    
                    <div style={{ marginBottom: '8px' }}>
                      <Text>Gravado:</Text>
                      <Text strong style={{ float: 'right' }}>{formatNumber(reporteData.ventas.gravado)}</Text>
                    </div>
                    
                    <div style={{ borderTop: '1px solid #d9d9d9', paddingTop: '8px', marginTop: '15px' }}>
                      <Text strong>Total:</Text>
                      <Text strong style={{ float: 'right', fontSize: '16px' }}>{formatNumber(reporteData.ventas.total)}</Text>
                    </div>
                  </div>
                </Col>
              </Row>

              <Row style={{ marginTop: '20px' }}>
                <Col span={24}>
                  <div style={{ backgroundColor: '#f8f5f0', padding: '15px', borderRadius: '6px', border: '1px solid #c69c6d' }}>
                    <Title level={5} style={{ margin: '0 0 15px 0', color: '#8b5a2b' }}>DIFERENCIA</Title>
                    
                    <Row>
                      <Col span={12}>
                        <div style={{ marginBottom: '8px' }}>
                          <Text>Cantidad de días:</Text>
                          <Text strong style={{ marginLeft: '10px' }}>{reporteData.diferencia.cantidad_dias}</Text>
                        </div>
                        
                        <div style={{ marginBottom: '8px' }}>
                          <Text>Gravado:</Text>
                          <Text strong style={{ marginLeft: '10px', color: reporteData.diferencia.gravado >= 0 ? '#52c41a' : '#f5222d' }}>
                            {formatNumber(reporteData.diferencia.gravado)}
                          </Text>
                        </div>
                      </Col>
                      
                      <Col span={12}>
                        <div style={{ textAlign: 'right' }}>
                          <Text strong style={{ fontSize: '18px' }}>Total:</Text>
                          <Text strong style={{ 
                            marginLeft: '10px', 
                            fontSize: '18px',
                            color: reporteData.diferencia.total >= 0 ? '#52c41a' : '#f5222d'
                          }}>
                            {formatNumber(reporteData.diferencia.total)}
                          </Text>
                        </div>
                      </Col>
                    </Row>
                  </div>
                </Col>
              </Row>

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