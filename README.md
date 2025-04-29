# Sistema de Biblioteca Universitaria

Este es un sistema de gestión de préstamos para la biblioteca universitaria, implementado con Flask y FastAPI.

## Características

- Gestión de recursos (libros, revistas, material didáctico, equipos)
- Registro de estudiantes
- Sistema de préstamos y devoluciones
- Consulta de préstamos por estudiante
- Autenticación de usuarios
- API REST con FastAPI
- Interfaz web con Flask

## Requisitos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- PowerShell (para Windows)

## Instalación

1. Clonar o descargar este repositorio
2. Abrir PowerShell y navegar al directorio del proyecto
3. Ejecutar el script de configuración:

```powershell
.\setup.ps1
```

Este script:
- Crea los directorios necesarios
- Configura un entorno virtual
- Instala las dependencias
- Inicializa la base de datos

## Uso

Para iniciar la aplicación:

```powershell
python run.py
```

Esto iniciará:
- La aplicación web Flask (interfaz de usuario)
- La API FastAPI (backend)

### Credenciales por defecto

- Usuario: admin
- Contraseña: admin123

**Importante**: Cambiar estas credenciales en producción.

## Estructura del Proyecto

```
biblioteca_universitaria/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── __init__.py
│   ├── models.py
│   ├── app.py
│   └── api.py
│
├── instance/
│   └── biblioteca.db
│
├── requirements.txt
├── setup.ps1
├── init_db.py
├── run.py
└── README.md
```

## API Endpoints

La API proporciona los siguientes endpoints:

- POST /token - Autenticación
- POST /recursos/ - Crear nuevo recurso
- POST /estudiantes/ - Registrar nuevo estudiante
- POST /prestamos/ - Crear nuevo préstamo
- GET /prestamos/estudiante/{id} - Consultar préstamos de un estudiante
- PUT /prestamos/{id}/devolver - Devolver un préstamo

## Seguridad

- Autenticación basada en tokens JWT
- Protección de rutas sensibles
- Validación de datos de entrada
- Manejo seguro de contraseñas

## Despliegue

La aplicación está configurada para desplegarse en Render:

1. Conectar el repositorio a Render
2. Configurar como Web Service
3. Usar `gunicorn app:app` como comando de inicio
4. Configurar las variables de entorno necesarias

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu función (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request
