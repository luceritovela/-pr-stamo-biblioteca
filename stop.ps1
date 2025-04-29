# Detener procesos en los puertos 5000 y 8000
Write-Host "Deteniendo la aplicación..."

$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($port5000) {
    Stop-Process -Id (Get-Process -Id $port5000.OwningProcess).Id -Force
    Write-Host "Detenido proceso en puerto 5000"
}

if ($port8000) {
    Stop-Process -Id (Get-Process -Id $port8000.OwningProcess).Id -Force
    Write-Host "Detenido proceso en puerto 8000"
}

Write-Host "Aplicación detenida correctamente"
