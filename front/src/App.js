import './App.css';
import AppRoutes from './Routes/Routes';
import { ChakraProvider } from '@chakra-ui/react';
import { FarmaciaProvider } from './context/FarmaciaContext';

function App() {
  return (
    <ChakraProvider>
      <FarmaciaProvider>
        <div className="App">
          <AppRoutes />
        </div>
      </FarmaciaProvider>
    </ChakraProvider>
  );
}

export default App;
