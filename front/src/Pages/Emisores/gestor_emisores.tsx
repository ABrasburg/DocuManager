import React, { useState, useEffect } from 'react';
import { Table, Button, message, Space } from 'antd';
import { FormOutlined } from "@ant-design/icons";
import '@inovua/reactdatagrid-community/index.css';
import  '../Comprobantes/gestor_comprobantes.css';

import Navbar from '../Utils/navbar';
import ModificarEmisor from './Popup/modificar_emisor';

interface Emisor {
  id: number;
  tipo_doc: string;
  cuit: string;
  denominacion: string;
}

const GestorEmisores: React.FC = () => {
    const [emisores, setEmisores] = useState<Emisor[]>([]);
    const [loading, setLoading] = useState(false);
    const [crear, setCrear] = useState(false);
    const [editar, setEditar] = useState(false);
    const [emisor, setEmisor] = useState<Emisor>({ id: 0, tipo_doc: '', cuit: '', denominacion: '' });

    const [mostrarEmisor, setMostrarEmisor] = useState(false);
    
    const fetchEmisores = async () => {
        setLoading(true);
        try {
        const response = await fetch('http://localhost:9000/emisores');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setEmisores(data);
        } catch (error) {
        message.error('Error fetching emisores');
        } finally {
        setLoading(false);
        }
    };

    useEffect(() => {
        fetchEmisores();
    }, []);

    const handleCreate = async () => {
        setLoading(true);
        setCrear(true);
        setEditar(false);
        setMostrarEmisor(true);
    };

    const handleUpdate = async (emisorEditar: Emisor) => {
        setLoading(true);
        setEditar(true);
        setCrear(false);
        setMostrarEmisor(true);
        setEmisor(emisorEditar);
    };

    return (
        <div>
            <Navbar />
            <div className="container">
                <h1 style={{ fontSize: '24px', fontWeight: 'bold', textAlign: 'center', marginBottom: '20px' }}>
                    Gestor de Emisores
                </h1>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                    <Button type="primary" onClick={() => handleCreate()}>
                        Crear Emisor
                    </Button>
                </div>
                <Table
                    rowKey="id"
                    dataSource={emisores}
                    loading={loading}
                    columns={[
                        { title: 'CUIT', dataIndex: 'cuit', key: 'cuit' },
                        { title: 'Denominación', dataIndex: 'denominacion', key: 'denominacion' },
                        {
                            title: 'Acciones',
                            key: 'acciones',
                            render: (text, record) => (
                                <Space size="middle">
                                    <Button icon={<FormOutlined />} onClick={() => handleUpdate(record)} />
                                </Space>
                            ),
                        },
                    ]}
                />
            </div>
            <ModificarEmisor
                open={mostrarEmisor}
                onClose={() => {
                    setCrear(false);
                    setEditar(false);
                    setLoading(false);
                    setMostrarEmisor(false);
                    fetchEmisores();
                    setEmisor({ id: 0, tipo_doc: '', cuit: '', denominacion: '' });
                }}
                emisor={emisor}
                onCreate={handleCreate}
                onEdit={handleUpdate}
                editar={editar}
                nuevo={crear}
            />
        </div>
    );
}
export default GestorEmisores;