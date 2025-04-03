import React from 'react';
import './App.css';
import GestorComprobantes from './Pages/Comprobantes/gestor_comprobantes';
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Sistema de Gestión de Comprobantes</h1>
      </header>
      <main className="App-content">
        <GestorComprobantes />
      </main>
    </div>
  );
}

export default App;