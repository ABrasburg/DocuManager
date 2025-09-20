@echo off
echo ========================================
echo   DocuManager - Instalacion Windows
echo ========================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Este script requiere privilegios de administrador
    echo Ejecutar como "Ejecutar como administrador"
    pause
    exit /b 1
)

echo 1. Verificando archivos necesarios...
if not exist "%~dp0back\start_backend.bat" (
    echo ERROR: No se encuentra start_backend.bat en la carpeta back
    pause
    exit /b 1
)
if not exist "%~dp0front\start_frontend.bat" (
    echo ERROR: No se encuentra start_frontend.bat en la carpeta front
    pause
    exit /b 1
)
echo Archivos encontrados correctamente.

echo.
echo 2. Verificando NSSM...
cd /d "%~dp0"
if not exist "nssm.exe" (
    echo Descarga NSSM manualmente desde: https://nssm.cc/download
    echo Coloca nssm.exe en la carpeta raiz del proyecto
    pause
)

echo.
echo 3. Creando carpeta de logs...
mkdir "%~dp0logs" 2>nul

echo.
echo 4. Creando servicio DocuManager Backend...
nssm install DocuManagerBack "%~dp0back\start_backend.bat"
nssm set DocuManagerBack DisplayName "DocuManager Backend"
nssm set DocuManagerBack Description "Servicio backend para DocuManager - Sistema de gestion de comprobantes"
nssm set DocuManagerBack Start SERVICE_AUTO_START
nssm set DocuManagerBack AppStdout "%~dp0logs\backend_out.log"
nssm set DocuManagerBack AppStderr "%~dp0logs\backend_err.log"

echo.
echo 5. Creando servicio DocuManager Frontend...
nssm install DocuManagerFront "%~dp0front\start_frontend.bat"
nssm set DocuManagerFront DisplayName "DocuManager Frontend"
nssm set DocuManagerFront Description "Servicio frontend para DocuManager"
nssm set DocuManagerFront Start SERVICE_AUTO_START
nssm set DocuManagerFront AppStdout "%~dp0logs\frontend_out.log"
nssm set DocuManagerFront AppStderr "%~dp0logs\frontend_err.log"

echo.
echo 6. Configurando archivo hosts...
echo # DocuManager Local Access >> C:\Windows\System32\drivers\etc\hosts
echo 127.0.0.1 documanager.local >> C:\Windows\System32\drivers\etc\hosts

echo.
echo 7. Iniciando servicios...
nssm start DocuManagerBack
nssm start DocuManagerFront

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Backend disponible en: http://documanager.local:9000
echo Frontend disponible en: http://documanager.local:3000
echo.
echo Para administrar los servicios:
echo - services.msc (Consola de servicios Windows)
echo - nssm edit DocuManagerBack
echo - nssm edit DocuManagerFront
echo.
pause