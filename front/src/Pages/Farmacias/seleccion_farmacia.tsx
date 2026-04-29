import React, { useEffect, useState } from 'react';
import { Button, Input, Spin, Typography } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useFarmacia } from '../../context/FarmaciaContext';
import { useNavigate } from 'react-router-dom';
import api from '../../api';

const { Title } = Typography;

interface Farmacia {
  id: number;
  nombre: string;
}

const SeleccionFarmacia: React.FC = () => {
  const { setFarmacia } = useFarmacia();
  const navigate = useNavigate();
  const [farmacias, setFarmacias] = useState<Farmacia[]>([]);
  const [loading, setLoading] = useState(true);
  const [creando, setCreando] = useState(false);
  const [nombreNueva, setNombreNueva] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/farmacias')
      .then((res) => setFarmacias(res.data))
      .catch(() => setError('No se pudo conectar al servidor.'))
      .finally(() => setLoading(false));
  }, []);

  const handleCrear = async () => {
    const nombre = nombreNueva.trim();
    if (!nombre) return;
    setCreando(true);
    try {
      const res = await api.post('/farmacia', { nombre });
      const nueva = res.data;
      setFarmacias((prev) => [...prev, nueva]);
      setNombreNueva('');
    } catch {
      setError('No se pudo crear la farmacia.');
    } finally {
      setCreando(false);
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <Title level={3} style={{ textAlign: 'center', marginBottom: 8 }}>
          DocuManager
        </Title>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: 32 }}>
          Seleccioná una farmacia para continuar
        </p>

        {error && (
          <p style={{ color: 'red', textAlign: 'center', marginBottom: 16 }}>{error}</p>
        )}

        <div style={styles.lista}>
          {farmacias.map((f) => (
            <button key={f.id} style={styles.botonFarmacia} onClick={() => { setFarmacia(f); navigate('/app'); }}>
              {f.nombre}
            </button>
          ))}
        </div>

        <div style={styles.nuevaFarmacia}>
          <Input
            placeholder="Nombre de nueva farmacia"
            value={nombreNueva}
            onChange={(e) => setNombreNueva(e.target.value)}
            onPressEnter={handleCrear}
            style={{ flex: 1 }}
          />
          <Button
            type="dashed"
            icon={<PlusOutlined />}
            loading={creando}
            onClick={handleCrear}
            disabled={!nombreNueva.trim()}
          >
            Crear
          </Button>
        </div>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#f0f2f5',
  },
  card: {
    background: '#fff',
    borderRadius: 12,
    padding: '40px 48px',
    width: 380,
    boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
  },
  lista: {
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
    marginBottom: 24,
  },
  botonFarmacia: {
    padding: '14px 20px',
    borderRadius: 8,
    border: '1.5px solid #d9d9d9',
    background: '#fff',
    fontSize: 16,
    cursor: 'pointer',
    textAlign: 'left',
    transition: 'all 0.15s',
  },
  nuevaFarmacia: {
    display: 'flex',
    gap: 8,
  },
};

export default SeleccionFarmacia;
