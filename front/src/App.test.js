import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock('./api', () => ({
  __esModule: true,
  default: {
    get: jest.fn(() => Promise.resolve({ data: [{ id: 1, nombre: 'Farmacia Test' }] })),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

beforeEach(() => {
  localStorage.clear();
  window.history.pushState({}, '', '/');
});

test('muestra la seleccion de farmacia al iniciar sin farmacia guardada', async () => {
  render(<App />);

  expect(await screen.findByText('DocuManager')).toBeInTheDocument();
  expect(screen.getByText('Seleccioná una farmacia para continuar')).toBeInTheDocument();
  expect(screen.getByText('Farmacia Test')).toBeInTheDocument();
});
