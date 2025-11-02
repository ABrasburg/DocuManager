import React, { useState, useEffect } from 'react';
import { Table, Button, message, DatePicker, Space, Spin, Tag } from 'antd';
import { SettingOutlined, DownloadOutlined, DollarOutlined } from "@ant-design/icons";
import dayjs from 'dayjs';
import '@inovua/reactdatagrid-community/index.css';

import api from  '../../api'
import { formatCurrency } from '../../Utils/formatNumber'

import Navbar from '../Utils/navbar';
import SetCuentaCorriente from './Popup/set_cuenta_corrientes';
import DescargarCuentaCorriente from './Popup/descargar_cuenta_corriente';
import MarcarPagado from './Popup/marcar_pagado';

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
    fecha_pago?: string;
    numero_ticket?: string;
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
    cuenta_corriente: boolean;
  }


const GestorCuentaCorriente: React.FC = () => {
    const [comprobantes, setComprobantes] = React.useState<Comprobante[]>([]);
    const [emisoresCuentaCorrientes, setEmisoresCuentaCorrientes] = React.useState<Emisor[]>([]);
    const [emisores, setEmisores] = React.useState<Emisor[]>([]);
    const [tiposComprobantes, setTiposComprobantes] = React.useState<any[]>([]);
    const [fechaInicioFiltro, setFechaInicioFiltro] = React.useState<string | null>(null);
    const [fechaFinFiltro, setFechaFinFiltro] = React.useState<string | null>(null);

    const [isOpen, setIsOpen] = useState(false);
    const [isDownloadOpen, setIsDownloadOpen] = useState(false);
    const [isPagadoModalOpen, setIsPagadoModalOpen] = useState(false);
    const [selectedComprobante, setSelectedComprobante] = useState<Comprobante | null>(null);

    useEffect(() => {
        fetchComprobantes();
    }, []);

    const fetchComprobantes = async () => {
        try {
          setLoadingComprobantes(true);
          const response1 = await api.get('/emisores');
          const emisoresData = response1.data;
          setEmisores(emisoresData || []);
          const response2 = await api.get('/comprobantes/cuenta_corriente');
          const data = response2.data;
          setComprobantes(data || []);
          setEmisoresCuentaCorrientes(
            data.reduce((acc: Emisor[], comprobante: Comprobante) => {
              if (!acc.some(e => e.cuit === comprobante.emisor.cuit)) {
                acc.push({ ...comprobante.emisor, cuenta_corriente: true });
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

    const handleSetCuentaCorriente = (cuit: string, cuentaCorriente: boolean) => {
        setEmisores(prevEmisores =>
          prevEmisores.map(emisor =>
            emisor.cuit === cuit ? { ...emisor, cuenta_corriente: cuentaCorriente } : emisor
          )
        );
      };

      const handleClosePopup = () => {
        setIsOpen(false);
        fetchComprobantes();
      };

      const handleMarcarPagado = (comprobante: Comprobante) => {
        setSelectedComprobante(comprobante);
        setIsPagadoModalOpen(true);
      };

      const handleClosePagadoModal = () => {
        setIsPagadoModalOpen(false);
        setSelectedComprobante(null);
      };

      const handlePagadoSuccess = () => {
        fetchComprobantes();
      };

    const isSameOrAfter = (date: string, start: string) => {
        return dayjs(date).isSame(start, 'day') || dayjs(date).isAfter(start, 'day');
      };
    
      const isSameOrBefore = (date: string, end: string) => {
        return dayjs(date).isSame(end, 'day') || dayjs(date).isBefore(end, 'day');
      };
    const [loadingComprobantes, setLoadingComprobantes] = React.useState<boolean>(true);
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
          filters: emisoresCuentaCorrientes.map((emisor: any) => ({ text: emisor.denominacion, value: emisor.cuit })),
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
          title: 'Estado Pago',
          key: 'estado_pago',
          render: (_: any, record: Comprobante) => (
            <div>
              {record.fecha_pago ? (
                <div>
                  <Tag color="green">Pagado</Tag>
                  <div style={{ fontSize: '11px', color: '#666' }}>
                    {record.fecha_pago}
                  </div>
                  {record.numero_ticket && (
                    <div style={{ fontSize: '11px', color: '#666' }}>
                      Ticket: {record.numero_ticket}
                    </div>
                  )}
                </div>
              ) : (
                <Tag color="orange">Pendiente</Tag>
              )}
            </div>
          ),
          filters: [
            { text: 'Pagado', value: 'pagado' },
            { text: 'Pendiente', value: 'pendiente' }
          ],
          onFilter: (value: any, record: Comprobante) => {
            if (value === 'pagado') return !!record.fecha_pago;
            if (value === 'pendiente') return !record.fecha_pago;
            return true;
          },
        },
        {
          title: 'Acciones',
          key: 'acciones',
          render: (_: any, record: Comprobante) => (
            <Space>
              {!record.fecha_pago && (
                <Button
                  type="primary"
                  size="small"
                  icon={<DollarOutlined />}
                  onClick={() => handleMarcarPagado(record)}
                >
                  Marcar Pagado
                </Button>
              )}
            </Space>
          ),
        }
      ];
    return (
        <div className="p-6 flex justify-center">
            <Navbar />
            <div className="w-full max-w-5xl bg-white shadow-lg rounded-2xl p-8 space-y-6">
                <h1 style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'center', marginBottom: '20px' }}>
                Gestión de Cuentas Corrientes
                </h1>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <Button
                            type="primary"
                            icon={<SettingOutlined />}
                            onClick={() => setIsOpen(true)}
                        >
                            Configurar Cuenta Corriente
                        </Button>
                        <Button
                            type="primary"
                            icon={<DownloadOutlined />}
                            onClick={() => setIsDownloadOpen(true)}
                        >
                            Descargar CSV
                        </Button>
                    </div>
                </div>
            </div>
            <Spin spinning={loadingComprobantes} tip="Cargando comprobantes...">
                <Table<Comprobante>
                    columns={columns}
                    dataSource={comprobantes}
                    size="middle"
                    pagination={{
                        showSizeChanger: true,
                        pageSizeOptions: ['10', '25', '50', '100'],
                        defaultPageSize: 10,
                        showTotal: (total, range) => `${range[0]}-${range[1]} de ${total} comprobantes`,
                    }}
                />
            </Spin>
            <SetCuentaCorriente
                isOpen={isOpen}
                onClose={handleClosePopup}
                emisores={emisores}
                onSetCuentaCorriente={handleSetCuentaCorriente}
            />
            <DescargarCuentaCorriente
                open={isDownloadOpen}
                onClose={() => setIsDownloadOpen(false)}
            />
            <MarcarPagado
                visible={isPagadoModalOpen}
                onClose={handleClosePagadoModal}
                comprobante={selectedComprobante}
                onSuccess={handlePagadoSuccess}
            />
        </div>
    );
};

export default GestorCuentaCorriente;