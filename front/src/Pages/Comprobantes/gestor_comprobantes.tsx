import React, { useState, useEffect } from 'react';
import { Table, Button, message, Upload, DatePicker, Space, Spin } from 'antd';
import { UploadOutlined, DeleteOutlined, MoreOutlined, FormOutlined, DownloadOutlined } from "@ant-design/icons";
import dayjs from 'dayjs';
import '@inovua/reactdatagrid-community/index.css';

import api from  '../../api'
import { formatCurrency } from '../../Utils/formatNumber'

import Navbar from '../Utils/navbar';
import ExitoPopup from '../Utils/exito_popup';
import ErrorPopup from '../Utils/error_popup';
import ComprobantePopup from './Popup/comprobante';
import ComprobanteEditPopup from './Popup/comprobante_edit';
import SumaPopup from './Popup/obtener_suma';
import DownloadComprobante from './Popup/descargar_comprobantes';

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

interface Emisor {
  cuit: string;
  denominacion: string;
}

const GestorComprobantes: React.FC = () => {
  const [loadingComprobantes, setLoadingComprobantes] = useState(false);
  const [textoError, setTextoError] = useState('');

  const [comprobantes, setComprobantes] = useState<Comprobante[]>([]);
  const [emisores, setEmisores] = useState<any[]>([]);
  const [tiposComprobantes, setTiposComprobantes] = useState<any[]>([]);
  const [fechaInicioFiltro, setFechaInicioFiltro] = useState<string | null>(null);
  const [fechaFinFiltro, setFechaFinFiltro] = useState<string | null>(null);

  const [comprobante, setComprobante] = useState<Comprobante | null>(null);
  const [mostrarPopupExito, setMostrarPopupExito] = useState(false);
  const [mostrarPopupError, setMostrarPopupError] = useState(false);
  const [mostrarPopupComprobante, setMostrarPopupComprobante] = useState(false);
  const [mostrarPopupComprobanteEdit, setMostrarPopupComprobanteEdit] = useState(false);
  const [mostrarPopupSuma, setMostrarPopupSuma] = useState(false);
  const [mostrarDownload, setMostrarDownload] = useState(false);

  useEffect(() => {
    setLoadingComprobantes(true);
    fetchComprobantes();
  }, []);

  const isSameOrAfter = (date: string, start: string) => {
    return dayjs(date).isSame(start, 'day') || dayjs(date).isAfter(start, 'day');
  };

  const isSameOrBefore = (date: string, end: string) => {
    return dayjs(date).isSame(end, 'day') || dayjs(date).isBefore(end, 'day');
  };

  const fetchComprobantes = async () => {
    try {
      setLoadingComprobantes(true);
      const response = await api.get('/comprobantes');
      const data = response.data;
      setComprobantes(data || []);
      setEmisores(
        data.reduce((acc: Emisor[], comprobante: Comprobante) => {
          if (!acc.some(e => e.cuit === comprobante.emisor.cuit)) {
            acc.push(comprobante.emisor);
          }
          return acc;
        }, [])
      );
      setTiposComprobantes(
        data.reduce((acc: any[], comprobante: Comprobante) => {
          if (!acc.some(e => e.nombre === comprobante.tipo_comprobante.nombre)) {
            acc.push(comprobante.tipo_comprobante);
          }
          return acc;
        }, [])
      );
    } catch (error) {
      setComprobantes([]);
      message.error('Error al cargar comprobantes');
    } finally {
      setLoadingComprobantes(false);
    }
  };

  const handleUpload = async (file: File) => {
    setLoadingComprobantes(true);
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      await api.post('/comprobantes/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      setMostrarPopupExito(true);
      fetchComprobantes();
  
    } catch (error: any) {
      const errorData = error.response?.data;
      setTextoError(errorData?.detail || 'Error desconocido');
      setMostrarPopupError(true);
    } finally {
      setLoadingComprobantes(false);
    }
  };

  const handleEdit = async (comprobante: Comprobante) => {
    try {
      const response = await api.put(`/comprobante/${comprobante.id}`, comprobante);
  
      if (response.status === 200) {
        message.success('Comprobante editado correctamente');
        fetchComprobantes();
      } else {
        message.error('Error al editar comprobante');
      }
    } catch (error) {
      message.error('Error al editar comprobante');
    }
  };  

  const columns = [
    {
      title: 'Fecha',
      dataIndex: 'fecha_emision',
      key: 'fecha',
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }: any) => (
        <div style={{ padding: 8 }}>
          <DatePicker.RangePicker
            value={selectedKeys && selectedKeys.length >= 2 ? [
              selectedKeys[0] ? dayjs(selectedKeys[0]) : null,
              selectedKeys[1] ? dayjs(selectedKeys[1]) : null
            ] : null}
            onChange={(dates) => {
                setSelectedKeys(dates);
                if (dates && dates.length >= 2) {
                    setFechaInicioFiltro(dates[0]?.format('YYYY-MM-DD') || null);
                    setFechaFinFiltro(dates[1]?.format('YYYY-MM-DD') || null);
                }
            }}
            format="YYYY-MM-DD"
          />
          <Space style={{ marginTop: 8 }}>
            <Button
              type="primary"
              onClick={() => confirm()}
              size="small"
            >
              Filtrar
            </Button>
            <Button
              onClick={() => {
                clearFilters?.();
                confirm();
              }}
              size="small"
            >
              Reiniciar
            </Button>
          </Space>
        </div>
      ),
      onFilter: (value: any, record: Comprobante) => {
        const fecha = dayjs(record.fecha_emision);
        const start = fechaInicioFiltro;
        const end = fechaFinFiltro;
        
        let cumpleStart = true;
        let cumpleEnd = true;
        
        if (start) cumpleStart = isSameOrAfter(fecha.toString(), start.toString());
        if (end) cumpleEnd = isSameOrBefore(fecha.toString(), end.toString());
        
        return cumpleStart && cumpleEnd;
      },
    },
    {
        title:  "Tipo de Comprobante",
        dataIndex: 'tipo_comprobante',
        key: 'tipo_comprobante',
        render: (_: any, record: Comprobante) => (
          <div>{record.tipo_comprobante?.nombre || 'N/A'}</div>
        ),
        filters: tiposComprobantes.map((tipo: any) => ({ text: tipo.nombre, value: tipo.nombre })),
        onFilter: (value: any, record: Comprobante) => record.tipo_comprobante.nombre === value,
    },
    {
        title: 'Punto de Venta',
        dataIndex: 'punto_venta',
        key: 'punto_venta',
    },
    {
        title: 'Número Desde',
        dataIndex: 'numero_desde',
        key: 'numero_desde',
    },
    {
      title: 'Emisor',
      key: 'emisor',
      render: (_: any, record: Comprobante) => (
        <div>
          <div>{record.emisor?.denominacion || 'N/A'}</div>
        </div>
      ),
      filters: emisores.map((emisor: any) => ({ text: emisor.denominacion, value: emisor.cuit })),
      onFilter: (value: any, record: Comprobante) => record.emisor.cuit === value,
    },
    {
      title: 'Total',
      dataIndex: 'total',
      key: 'total',
      render: (total: number, record: Comprobante) => {
        const signo = record.tipo_comprobante?.nombre === "Nota de Crédito" ? -1 : 1;
        const totalConSigno = signo * (total || 0);
        return formatCurrency(totalConSigno);
      },
    },
    {
        title: 'Acciones',
        key: 'acciones',
        render: (_: any, record: Comprobante) => (
          <div>
            <Button
                icon={<FormOutlined />}
                onClick={async () => {
                    try {
                      const response = await fetch(`http://localhost:9000/comprobante/${record.id}`);
                      if (response.ok) {
                        const data = await response.json();
                        setComprobante(data);
                        setMostrarPopupComprobanteEdit(true);
                      } else {
                        message.error('Error al cargar comprobante');
                      }
                    }
                    catch (error) {
                      message.error('Error al cargar comprobante');
                    }
                }}
            />
            <Button
              icon={<DeleteOutlined />}
              onClick={async () => {
                try {
                  const response = await fetch(`http://localhost:9000/comprobante/${record.id}`, {
                    method: 'DELETE',
                  });

                  if (response.ok) {
                    message.success('Comprobante eliminado');
                    await fetchComprobantes();
                  } else {
                    const errorData = await response.json();
                    message.error(`Error al eliminar: ${errorData.detail || 'Error desconocido'}`);
                  }
                } catch (error) {
                  message.error('Error al eliminar comprobante');
                }
              }}
            />
            <Button
                icon={<MoreOutlined />}
                onClick={async () => {
                    try {
                      const response = await fetch(`http://localhost:9000/comprobante/${record.id}`);
                      if (response.ok) {
                        const data = await response.json();
                        setComprobante(data);
                        setMostrarPopupComprobante(true);
                      } else {
                        message.error('Error al cargar comprobante');
                      }
                    }
                    catch (error) {
                      message.error('Error al cargar comprobante');
                    }
                }}
            />
          </div>
        ),
    }
  ];
  
  return (
    <div className="p-6 flex justify-center">
      <Navbar />
      <div className="w-full max-w-5xl bg-white shadow-lg rounded-2xl p-8 space-y-6">
        <h1 style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'center', marginBottom: '20px' }}>
          Gestión de Comprobantes
        </h1>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <Upload
              accept=".csv"
              showUploadList={false}
              beforeUpload={(file) => {
                handleUpload(file);
                return false;
              }}
              maxCount={1}
            >
              <Button icon={<UploadOutlined />} type="primary">
                Cargar Comprobante
              </Button>
            </Upload>
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={() => setMostrarDownload(true)}
            >
              Descargar Comprobantes
            </Button>
            <DownloadComprobante
              open={mostrarDownload}
              onClose={() => setMostrarDownload(false)}
            />
          </div>
          <Button
            type="primary"
            onClick={() => setMostrarPopupSuma(true)}
          >
            Obtener Suma
          </Button>
        </div>
      </div>
      <Spin spinning={loadingComprobantes} tip="Cargando comprobantes...">
          <Table<Comprobante> columns={columns} dataSource={comprobantes} size="middle" />
      </Spin>
      <ExitoPopup
        open={mostrarPopupExito}
        onClose={() => setMostrarPopupExito(false)}
        texto="Comprobantes cargados correctamente"
      />
      <ErrorPopup
        open={mostrarPopupError}
        onClose={() => setMostrarPopupError(false)}
        texto={textoError}
      />
      <ComprobantePopup
        comprobante={comprobante}
        open={mostrarPopupComprobante}
        onClose={() => setMostrarPopupComprobante(false)}
      />
      <ComprobanteEditPopup
        comprobante={comprobante}
        open={mostrarPopupComprobanteEdit}
        onClose={() => setMostrarPopupComprobanteEdit(false)}
        handleSave={handleEdit}
      />
      <SumaPopup
        open={mostrarPopupSuma}
        onClose={() => setMostrarPopupSuma(false)}
        />
    </div>
  );
};

export default GestorComprobantes;