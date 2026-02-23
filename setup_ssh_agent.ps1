# Script para configurar SSH Agent en Windows
# Ejecutar como Administrador: Right-click > "Run as Administrator"

Write-Host "Configurando SSH Agent en Windows..." -ForegroundColor Green

# Verificar si OpenSSH está instalado
$opensshClient = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*'
$opensshServer = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'

if ($opensshClient.State -ne "Installed") {
    Write-Host "Instalando OpenSSH Client..." -ForegroundColor Yellow
    Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
}

# Verificar el servicio SSH Agent
$service = Get-Service -Name ssh-agent -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "Configurando servicio SSH Agent..." -ForegroundColor Yellow
    
    # Configurar para inicio automático
    Set-Service -Name ssh-agent -StartupType Automatic
    
    # Iniciar el servicio
    Start-Service ssh-agent
    
    Write-Host "Servicio SSH Agent configurado e iniciado." -ForegroundColor Green
} else {
    Write-Host "El servicio ssh-agent no está disponible." -ForegroundColor Red
    Write-Host "Esto puede ser normal en algunas versiones de Windows." -ForegroundColor Yellow
    Write-Host "Usaremos el método alternativo con ssh-add." -ForegroundColor Yellow
}

# Verificar claves SSH existentes
Write-Host "`nVerificando claves SSH..." -ForegroundColor Yellow
$sshKeys = Get-ChildItem -Path $env:USERPROFILE\.ssh\*.pub -ErrorAction SilentlyContinue

if ($sshKeys) {
    Write-Host "Claves encontradas:" -ForegroundColor Green
    foreach ($key in $sshKeys) {
        Write-Host "  - $($key.Name)" -ForegroundColor Cyan
    }
    
    Write-Host "`nPara agregar tus claves al agente, ejecuta:" -ForegroundColor Yellow
    Write-Host "  ssh-add ~\.ssh\id_ed25519" -ForegroundColor White
    Write-Host "  (o la ruta de tu clave privada)" -ForegroundColor Gray
} else {
    Write-Host "No se encontraron claves SSH públicas en ~\.ssh\" -ForegroundColor Yellow
}

Write-Host "`nConfiguración completada!" -ForegroundColor Green
Write-Host "`nPróximos pasos:" -ForegroundColor Yellow
Write-Host "1. Agrega tus claves al agente con: ssh-add ~\.ssh\tu_clave_privada" -ForegroundColor White
Write-Host "2. La passphrase se pedirá una vez y se guardará en la sesión" -ForegroundColor White
Write-Host "3. Para hacerlo permanente, agrega las claves al perfil de PowerShell" -ForegroundColor White


