# Configuración de SSH Agent en Windows

Esta guía te ayudará a configurar el agente SSH en Windows para evitar ingresar la passphrase cada vez.

## Método 1: Configuración Automática (Recomendado)

### Paso 1: Ejecutar script de configuración (como Administrador)

1. Abre PowerShell como **Administrador** (Right-click > "Run as Administrator")
2. Navega a tu proyecto:
   ```powershell
   cd C:\Users\juana\PycharmProjects\tesis-umpe-supermarket-stock-prediction
   ```
3. Ejecuta el script:
   ```powershell
   .\setup_ssh_agent.ps1
   ```

### Paso 2: Agregar tus claves al agente

Ejecuta el script para agregar tus claves:
```powershell
.\add_ssh_keys.ps1
```

O manualmente:
```powershell
ssh-add ~\.ssh\id_ed25519
# Ingresa tu passphrase una vez
```

### Paso 3: Hacer permanente (Opcional)

Para que las claves se agreguen automáticamente en cada sesión, agrega al perfil de PowerShell:

1. Abre tu perfil de PowerShell:
   ```powershell
   notepad $PROFILE
   ```
   
2. Si el archivo no existe, créalo:
   ```powershell
   New-Item -Path $PROFILE -Type File -Force
   notepad $PROFILE
   ```

3. Agrega esta línea al final del archivo:
   ```powershell
   ssh-add ~\.ssh\id_ed25519 2>$null
   ```

## Método 2: Configuración Manual

### Paso 1: Verificar servicio SSH Agent

```powershell
Get-Service ssh-agent
```

### Paso 2: Configurar inicio automático

```powershell
# Como Administrador
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

### Paso 3: Agregar claves

```powershell
ssh-add ~\.ssh\id_ed25519
```

## Método 3: Usar Git Credential Manager (Alternativa)

Si prefieres usar HTTPS en lugar de SSH:

```powershell
git config --global credential.helper manager-core
```

## Verificación

Verifica que las claves estén agregadas:

```powershell
ssh-add -l
```

Deberías ver tus claves listadas.

## Solución de Problemas

### El servicio ssh-agent no existe

En algunas versiones de Windows, el servicio puede no estar disponible. En ese caso:

1. Usa `ssh-add` directamente (funciona sin el servicio)
2. Agrega las claves manualmente en cada sesión
3. O usa el método del perfil de PowerShell

### Las claves se pierden al cerrar la terminal

Esto es normal. Para hacerlo permanente:
- Agrega `ssh-add` a tu perfil de PowerShell (ver Método 1, Paso 3)
- O usa un script de inicio automático

### Cursor no reconoce las claves

1. Asegúrate de que Cursor esté usando el terminal integrado
2. Verifica que `git.terminalAuthentication` esté habilitado en Cursor
3. Reinicia Cursor después de configurar el agente

## Notas

- La passphrase se guarda en memoria durante la sesión
- Al cerrar PowerShell, las claves se eliminan del agente
- Para persistencia, usa el perfil de PowerShell o un script de inicio


