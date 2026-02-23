# Script para agregar claves SSH al agente
# Ejecutar en cada sesión o agregar al perfil de PowerShell

Write-Host "Agregando claves SSH al agente..." -ForegroundColor Green

# Buscar claves privadas comunes
$commonKeys = @(
    "$env:USERPROFILE\.ssh\id_ed25519",
    "$env:USERPROFILE\.ssh\id_rsa",
    "$env:USERPROFILE\.ssh\id_ecdsa"
)

$keysAdded = $false

foreach ($keyPath in $commonKeys) {
    if (Test-Path $keyPath) {
        Write-Host "Agregando clave: $keyPath" -ForegroundColor Yellow
        ssh-add $keyPath
        if ($LASTEXITCODE -eq 0) {
            $keysAdded = $true
        }
    }
}

if (-not $keysAdded) {
    Write-Host "No se encontraron claves SSH estándar." -ForegroundColor Yellow
    Write-Host "Agrega manualmente con: ssh-add ~\.ssh\tu_clave_privada" -ForegroundColor White
} else {
    Write-Host "`nClaves agregadas exitosamente!" -ForegroundColor Green
    Write-Host "Verificando claves en el agente:" -ForegroundColor Yellow
    ssh-add -l
}


