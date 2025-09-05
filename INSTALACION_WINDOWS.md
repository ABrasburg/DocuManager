# Instalación DocuManager en Windows

## Requisitos Previos

- **Windows 10/11** con privilegios de administrador
- **Python 3.9+** instalado y en PATH
- **Node.js 16+** instalado y en PATH
- **Git** (opcional, para clonar el repositorio)

## Instalación Automática

### 1. Descargar NSSM
1. Ir a https://nssm.cc/download
2. Descargar la versión apropiada (32-bit o 64-bit)
3. Extraer `nssm.exe` en la carpeta raíz del proyecto

### 2. Ejecutar Instalación
1. **Clic derecho** en `install_windows.bat`
2. Seleccionar **"Ejecutar como administrador"**
3. Seguir las instrucciones en pantalla

### 3. Verificación
- Backend: http://documanager.local:9000
- Frontend: http://documanager.local:3000
- Documentación API: http://documanager.local:9000/docs

## Configuración de Red

### Para acceder desde otros equipos de la red:

1. **En la máquina Windows (servidor):**
   - Obtener IP: `ipconfig` 
   - Ejemplo: `192.168.1.100`

2. **En cada equipo cliente:**
   - **Windows:** Editar `C:\Windows\System32\drivers\etc\hosts`
   - **Mac/Linux:** Editar `/etc/hosts`
   - Agregar línea: `192.168.1.100 documanager.local`

## Administración de Servicios

### Consola de Windows:
```cmd
services.msc
```
Buscar: "DocuManager Backend" y "DocuManager Frontend"

### Comandos NSSM:
```cmd
# Ver estado
nssm status DocuManagerBack
nssm status DocuManagerFront

# Detener
nssm stop DocuManagerBack
nssm stop DocuManagerFront

# Iniciar
nssm start DocuManagerBack  
nssm start DocuManagerFront

# Editar configuración
nssm edit DocuManagerBack
```

## Logs y Troubleshooting

### Ubicación de logs:
- Backend: `back/logs/` (si configurado)
- Frontend: Eventos de Windows
- NSSM: Visor de eventos Windows > Aplicaciones

### Problemas Comunes:

**Puerto ocupado:**
```cmd
netstat -ano | findstr :9000
netstat -ano | findstr :3000
```

**Permisos:**
- Ejecutar scripts como administrador
- Verificar permisos de carpeta del proyecto

**Firewall:**
- Permitir puertos 3000 y 9000 en Windows Firewall

## Desinstalación

Ejecutar `uninstall_windows.bat` **como administrador**

## Estructura Final

```
DocuManager/
├── install_windows.bat     # Script de instalación
├── uninstall_windows.bat   # Script de desinstalación  
├── nssm.exe               # Administrador de servicios
├── back/                  # Backend FastAPI
├── front/                 # Frontend React
└── INSTALACION_WINDOWS.md # Esta documentación
```