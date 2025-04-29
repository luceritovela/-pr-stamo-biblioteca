# Crear directorios necesarios
$directories = @(
    "instance",
    "app",
    "app/static",
    "app/static/css",
    "app/static/js",
    "app/templates"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
}

# Configurar entorno virtual
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activar entorno virtual
.\venv\Scripts\Activate

# Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# Inicializar la base de datos
python init_db.py
