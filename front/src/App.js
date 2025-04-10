import React from 'react';
import './App.css';
import GestorComprobantes from './Pages/Comprobantes/gestor_comprobantes';
import Logo from "./Imagenes/Logo.png";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={Logo} className="App-logo" alt="logo" style={{ height: '11em' }} />
      </header>
      <main className="App-content">
        <GestorComprobantes />
      </main>
    </div>
  );
}

export default App;