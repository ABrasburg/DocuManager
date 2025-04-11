import React from 'react';

import Navbar from '../Utils/navbar';


const GestorCuentaCorriente: React.FC = () => {
    return (
        <div className="p-6 flex justify-center">
            <Navbar />
            <h1>Gestor de Cuenta Corriente</h1>
            <p>Esta es una página genérica para probar. Modifícala según tus necesidades.</p>
        </div>
    );
};

export default GestorCuentaCorriente;