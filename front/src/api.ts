import axios from 'axios';

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

const api = axios.create({
  baseURL: isLocal ? `http://${window.location.hostname}:9000` : '/api',
});

api.interceptors.request.use((config) => {
  try {
    const stored = localStorage.getItem('farmacia');
    if (stored) {
      const farmacia = JSON.parse(stored);
      config.params = { ...config.params, farmacia_id: farmacia.id };
    }
  } catch {
    // si localStorage falla, seguimos sin farmacia_id
  }
  return config;
});

export default api;
