import React, { useState } from 'react';
import './navbar.css';
import { useNavigate } from "react-router-dom";
import Logo from '../../Imagenes/Logo.png';
import { useFarmacia } from '../../context/FarmaciaContext';

type LinkProps = {
  to: string;
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
};

const Link: React.FC<LinkProps> = ({ to, className, children, onClick }) => {
  const navigate = useNavigate();

  const handleClick = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    navigate(to);
    if (onClick) onClick();
  };

  return (
    <a href={to} className={className} onClick={handleClick}>
      {children}
    </a>
  );
};

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { farmacia, setFarmacia } = useFarmacia();
  const navigate = useNavigate();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  const handleCambiarFarmacia = () => {
    setFarmacia(null);
    navigate('/');
    closeMenu();
  };

  return (
    <nav className="navbar">
      <header className="navbar-left">
        <img src={Logo} className="App-logo" alt="logo" style={{ height: '11em' }} />
      </header>

      <button className="hamburger-menu" onClick={toggleMenu} aria-label="Toggle menu">
        <span className="hamburger-line"></span>
        <span className="hamburger-line"></span>
        <span className="hamburger-line"></span>
      </button>

      <div className={`navbar-right ${isMenuOpen ? 'active' : ''}`}>
        <Link to="/app/gestor_emisores" className="navbar-link" onClick={closeMenu}>Emisores</Link>
        <Link to="/app/gestor_cuenta_corriente" className="navbar-link" onClick={closeMenu}>Cuenta Corriente</Link>
        <Link to="/app/gestor_zetas" className="navbar-link" onClick={closeMenu}>Zetas</Link>
        <Link to="/app/gestor_comprobantes" className="navbar-link" onClick={closeMenu}>Comprobantes</Link>
        <Link to="/app/reporte_afip" className="navbar-link" onClick={closeMenu}>Reporte AFIP</Link>
        {farmacia && (
          <button
            className="navbar-link"
            onClick={handleCambiarFarmacia}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#888', fontSize: 'inherit' }}
          >
            {farmacia.nombre} ✕
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
