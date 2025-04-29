from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import bcrypt

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    prestamos = db.relationship('Prestamo', backref='estudiante', lazy=True)

class Recurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    prestamos = db.relationship('Prestamo', backref='recurso', lazy=True)

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    recurso_id = db.Column(db.Integer, db.ForeignKey('recurso.id'), nullable=False)
    estado = db.Column(db.String(20), default='activo')
