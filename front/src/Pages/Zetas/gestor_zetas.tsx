import React, { useState, useEffect } from 'react';
import { Table, Button, message, DatePicker, Space, Spin } from 'antd';
import { DeleteOutlined, FormOutlined, DownloadOutlined } from "@ant-design/icons";
import dayjs from 'dayjs';
import '@inovua/reactdatagrid-community/index.css';

import Navbar from '../Utils/navbar';
import ModificarZeta from './Popup/modificar_zeta';

import  api from '../../api';

interface Zeta {
    id: number;
    fecha: number;
    punto_venta: number;
    numero: number;
    ultimo_ticket: number;
    exento: number;
    iva: number;
    gravado: number;
    cuenta_corriente: string;
    total: number;
}

const GestorZetas: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [zetas, setZetas] = useState<any[]>([]);
    const [crear, setCrear] = useState(false);
    const [editar, setEditar] = useState(false);
    const [zeta, setZeta] = useState<Zeta>({
        id: 0,
        fecha: Date.now(),
        punto_venta: 0,
        numero: 0,
        ultimo_ticket: 0,
        exento: 0,
        iva: 0,
        gravado: 0,
        cuenta_corriente: '',
        total: 0,
    });

    const [fechaInicioFiltro, setFechaInicioFiltro] = useState<string | null>(null);
    const [fechaFinFiltro, setFechaFinFiltro] = useState<string | null>(null);

    const [mostrarUtilizarZeta, setMostrarUtilizarZeta] = useState(false);

    useEffect(() => {
        fetchZetas();
    }, []);

    const isSameOrAfter = (date: string, start: string) => {
        return dayjs(date).isSame(start, 'day') || dayjs(date).isAfter(start, 'day');
      };
    
    const isSameOrBefore = (date: string, end: string) => {
        return dayjs(date).isSame(end, 'day') || dayjs(date).isBefore(end, 'day');
    };

    const fetchZetas = async () => {
        setLoading(true);
        try {
          const response = await api.get('/zetas');
          setZetas(response.data);
        } catch (error) {
          message.error('Error fetching data');
        } finally {
          setLoading(false);
        }
      };      

    const handleCreate = async () => {
        setCrear(true);
        setMostrarUtilizarZeta(true);
        setZeta({
            id: 0,
            fecha: Date.now(),
            punto_venta: 0,
            numero: 0,
            ultimo_ticket: 0,
            exento: 0,
            iva: 0,
            gravado: 0,
            cuenta_corriente: '',
            total: 0,
        });
    };

    const handleUpdate = async (zetaEditar: Zeta) => {
        setEditar(true);
        setMostrarUtilizarZeta(true);
        setZeta(zetaEditar);
    };

    const handleDelete = async (id: number) => {
        setLoading(true);
        try {
          await api.delete(`/zeta/${id}`);
          message.success('Zeta eliminada');
          fetchZetas();
        } catch (error) {
          message.error('Error deleting data');
        } finally {
          setLoading(false);
        }
      };      

    const columns = [
        { 
            title: 'Fecha', 
            dataIndex: 'fecha', 
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
            onFilter: (value: any, record: Zeta) => {
                const fecha = dayjs(record.fecha);
                const start = fechaInicioFiltro;
                const end = fechaFinFiltro;
                    
                let cumpleStart = true;
                let cumpleEnd = true;
                    
                if (start) cumpleStart = isSameOrAfter(fecha.toString(), start.toString());
                if (end) cumpleEnd = isSameOrBefore(fecha.toString(), end.toString());
                    
                return cumpleStart && cumpleEnd;
            },
        },
        { title: 'Número', dataIndex: 'numero', key: 'numero' },
        { title: 'Último Ticket', dataIndex: 'ultimo_ticket', key: 'ultimo_ticket' },
        { title: 'Exento', dataIndex: 'exento', key: 'exento' },
        { title: 'IVA', dataIndex: 'iva', key: 'iva' },
        { title: 'Gravado', dataIndex: 'gravado', key: 'gravado' },
        { title: 'Cuenta Corriente', dataIndex: 'cuenta_corriente', key: 'cuenta_corriente' },
        { title: 'Total', dataIndex: 'total', key: 'total' },
        {
            title: 'Acciones',
            key: 'acciones',
            render: (text: string, record: Zeta) => (
                <Space size="middle">
                    <Button
                        icon={<FormOutlined />}
                        onClick={() => handleUpdate(record)}
                    />
                    <Button
                        icon={<DeleteOutlined />}
                        onClick={() => handleDelete(record.id)}
                    />
                </Space>
            ),
        },
    ];

    return (
        <div className="p-6 flex justify-center">
            <Navbar />
            <h1 style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'center', marginBottom: '20px' }}>
            Gestor de Zetas
            </h1>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
            <Button type="primary" onClick={() => handleCreate()}>
                Crear Zeta
            </Button>
            <Button type="primary" icon={<DownloadOutlined />} onClick={() => message.info('Descarga iniciada')}>
                Descargar
            </Button>
            </div>
            <Spin spinning={loading} tip="Cargando Zetas...">
            <Table<Zeta> columns={columns} dataSource={zetas} size="middle" />
            </Spin>
            <ModificarZeta
            open={mostrarUtilizarZeta}
            onClose={() => {
                setCrear(false);
                setEditar(false);
                setLoading(false);
                setMostrarUtilizarZeta(false);
                setZeta({
                id: 0,
                fecha: Date.now(),
                punto_venta: 0,
                numero: 0,
                ultimo_ticket: 0,
                exento: 0,
                iva: 0,
                gravado: 0,
                cuenta_corriente: '',
                total: 0,
                });
                fetchZetas();
            }}
            zeta={zeta}
            onCreate={handleCreate}
            onEdit={handleUpdate}
            editar={editar}
            nuevo={crear}
            />
        </div>
    );
};

export default GestorZetas;