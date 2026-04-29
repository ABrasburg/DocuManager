import React from "react";
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from "react-router-dom";
import GestorComprobantes from "../Pages/Comprobantes/gestor_comprobantes";
import GestorCuentaCorriente from "../Pages/Cuentas_Corrientes/gestor_cuenta_corriente";
import GestorEmisores from "../Pages/Emisores/gestor_emisores";
import GestorZetas from "../Pages/Zetas/gestor_zetas";
import ReporteAFIP from "../Pages/Reportes/reporte_afip";
import SeleccionFarmacia from "../Pages/Farmacias/seleccion_farmacia";
import { useFarmacia } from "../context/FarmaciaContext";

const ProtectedLayout: React.FC = () => {
  const { farmacia } = useFarmacia();
  if (!farmacia) return <Navigate to="/" replace />;
  return <Outlet />;
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <SeleccionFarmacia />,
  },
  {
    path: "/app",
    element: <ProtectedLayout />,
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

const AppRoutes: React.FC = () => <RouterProvider router={router} />;

export default AppRoutes;
