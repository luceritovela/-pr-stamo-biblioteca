from app.app import app
from app.models import db, Usuario

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario admin si no existe
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(username='admin', es_admin=True)
            admin.set_password('admin123')  # Cambiar en producción
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado exitosamente")

if __name__ == '__main__':
    init_db()
