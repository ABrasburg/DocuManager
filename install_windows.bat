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

echo 1. Instalando dependencias Python...
cd /d "%~dp0back"
pip install pipenv
pipenv install --deploy

echo.
echo 2. Instalando dependencias Node.js...
cd /d "%~dp0front"
npm install
npm run build

echo.
echo 3. Descargando NSSM...
cd /d "%~dp0"
if not exist "nssm.exe" (
    echo Descarga NSSM manualmente desde: https://nssm.cc/download
    echo Coloca nssm.exe en la carpeta raiz del proyecto
    pause
)

echo.
echo 4. Creando servicio DocuManager Backend...
nssm install DocuManagerBack pipenv
nssm set DocuManagerBack Parameters "run python main.py"
nssm set DocuManagerBack AppDirectory "%~dp0back"
nssm set DocuManagerBack DisplayName "DocuManager Backend"
nssm set DocuManagerBack Description "Servicio backend para DocuManager - Sistema de gestion de comprobantes"
nssm set DocuManagerBack Start SERVICE_AUTO_START

echo.
echo 5. Creando servicio DocuManager Frontend...
nssm install DocuManagerFront node
nssm set DocuManagerFront Parameters ".\node_modules\.bin\serve -s build -l 3000"
nssm set DocuManagerFront AppDirectory "%~dp0front"
nssm set DocuManagerFront DisplayName "DocuManager Frontend"
nssm set DocuManagerFront Description "Servicio frontend para DocuManager"
nssm set DocuManagerFront Start SERVICE_AUTO_START

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