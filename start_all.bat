@echo off
echo ========================================
echo   DocuManager - Iniciando Servicios
echo ========================================
echo.

echo Iniciando Backend...
start "DocuManager Backend" "%~dp0back\start_backend.bat"

echo Iniciando Frontend...
start "DocuManager Frontend" "%~dp0front\start_frontend.bat"

echo.
echo Ambos servicios iniciados.
echo Backend: http://localhost:9000
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul