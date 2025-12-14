import React, { useState } from 'react';
import './navbar.css';
import { useNavigate } from "react-router-dom";
import Logo from '../../Imagenes/Logo.png';

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

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
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
        <Link to="/gestor_emisores" className="navbar-link" onClick={closeMenu}>Emisores</Link>
        <Link to="/gestor_cuenta_corriente" className="navbar-link" onClick={closeMenu}>Cuenta Corriente</Link>
        <Link to="/gestor_zetas" className="navbar-link" onClick={closeMenu}>Zetas</Link>
        <Link to="/gestor_comprobantes" className="navbar-link" onClick={closeMenu}>Comprobantes</Link>
        <Link to="/reporte_afip" className="navbar-link" onClick={closeMenu}>Reporte AFIP</Link>
      </div>
    </nav>
  );
};

export default Navbar;
