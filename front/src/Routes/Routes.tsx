import React from "react";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import GestorComprobantes from "../Pages/Comprobantes/gestor_comprobantes";
import GestorCuentaCorriente from "../Pages/Cuentas_Corrientes/gestor_cuenta_corriente";

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
      { path: "gestor_cuenta_corriente", element: <GestorCuentaCorriente /> },
    ],
  },
]);

// Este componente envuelve el provider de rutas
const AppRoutes = () => <RouterProvider router={router} />;

export default AppRoutes;

