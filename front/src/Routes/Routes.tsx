import React from "react";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import GestorComprobantes from "../Pages/Comprobantes/gestor_comprobantes";
import GestorCuentaCorriente from "../Pages/Cuentas_Corrientes/gestor_cuenta_corriente";
import GestorEmisores from "../Pages/Emisores/gestor_emisores";
import GestorZetas from "../Pages/Zetas/gestor_zetas";
import ReporteAFIP from "../Pages/Reportes/reporte_afip";

// Este componente es el layout que envolverá las rutas hijas
const PageWrapper = () => {
  return (
    <>
      {/* Si querés agregar transiciones o animaciones, hacelo acá */}
      <Outlet />
    </>
  );
};

// Definimos las rutas
const router = createBrowserRouter([
  {
    path: "/",
    element: <PageWrapper />,
    children: [
      { path: "", element: <GestorComprobantes /> },
      { path: "gestor_comprobantes", element: <GestorComprobantes /> },
      { path: "gestor_zetas", element: <GestorZetas /> },
      { path: "gestor_emisores", element: <GestorEmisores /> },
      { path: "gestor_cuenta_corriente", element: <GestorCuentaCorriente /> },
      { path: "reporte_afip", element: <ReporteAFIP /> },
    ],
  },
]);

// Este componente envuelve el provider de rutas
const AppRoutes = () => <RouterProvider router={router} />;

export default AppRoutes;

