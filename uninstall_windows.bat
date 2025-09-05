@echo off
echo ========================================
echo   DocuManager - Desinstalacion Windows
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

echo 1. Deteniendo servicios...
nssm stop DocuManagerBack
nssm stop DocuManagerFront

echo.
echo 2. Eliminando servicios...
nssm remove DocuManagerBack confirm
nssm remove DocuManagerFront confirm

echo.
echo 3. Limpiando archivo hosts...
powershell -Command "(Get-Content C:\Windows\System32\drivers\etc\hosts) | Where-Object { $_ -notmatch 'documanager.local' -and $_ -notmatch '# DocuManager Local Access' } | Set-Content C:\Windows\System32\drivers\etc\hosts"

echo.
echo ========================================
echo   DESINSTALACION COMPLETADA
echo ========================================
echo.
echo Los archivos del proyecto no han sido eliminados.
echo Los servicios DocuManager han sido removidos del sistema.
echo.
pause