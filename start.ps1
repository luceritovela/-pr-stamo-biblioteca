# Verificar si el entorno virtual existe
if (-not (Test-Path "venv")) {
    Write-Host "El entorno virtual no existe. Ejecute setup.ps1 primero."
    exit 1
}

# Activar el entorno virtual y ejecutar la aplicación
Write-Host "`n======================================"
Write-Host "Iniciando Biblioteca Universitaria"
Write-Host "======================================`n"

Write-Host "Interfaces disponibles:"
Write-Host "- Web: http://localhost:5000"
Write-Host "- API: http://localhost:8000`n"

Write-Host "Para detener la aplicación:"
Write-Host "1. Presione Ctrl+C en esta ventana, o"
Write-Host "2. Ejecute .\stop.ps1 en otra terminal`n"

Write-Host "Iniciando servicios..."
Write-Host "--------------------------------------`n"

# Usar la ruta completa al intérprete de Python del entorno virtual
$pythonPath = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
& $pythonPath "run.py"
