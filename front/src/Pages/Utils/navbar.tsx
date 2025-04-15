import React from 'react';
import './navbar.css';
import { useNavigate } from "react-router-dom";
import Logo from '../../Imagenes/Logo.png';

type LinkProps = {
  to: string;
  className?: string;
  children: React.ReactNode;
};

const Link: React.FC<LinkProps> = ({ to, className, children }) => {
  const navigate = useNavigate();

  const handleClick = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    navigate(to); // usamos navigate en lugar de window.location.href para navegación sin recarga
  };

  return (
    <a href={to} className={className} onClick={handleClick}>
      {children}
    </a>
  );
};

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <header className="navbar-left">
        <img src={Logo} className="App-logo" alt="logo" style={{ height: '11em' }} />
      </header>
      <div className="navbar-right">
        <Link to="/gestor_comprobantes" className="navbar-link">Comprobantes</Link>
        <Link to="/gestor_cuenta_corriente" className="navbar-link">Cuenta Corriente</Link>
      </div>
    </nav>
  );
};

export default Navbar;
