from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session
import os
from .models import db, Usuario, Estudiante, Recurso, Prestamo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['es_admin'] = user.es_admin
            return redirect(url_for('dashboard'))
        
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    prestamos_activos = Prestamo.query.filter_by(estado='activo').all()
    recursos_disponibles = Recurso.query.filter_by(disponible=True).all()
    return render_template('dashboard.html', 
                         prestamos=prestamos_activos, 
                         recursos=recursos_disponibles)

@app.route('/recursos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_recurso():
    if not session.get('es_admin'):
        flash('No tiene permisos para esta acción')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        nuevo = Recurso(nombre=nombre, tipo=tipo)
        db.session.add(nuevo)
        db.session.commit()
        flash('Recurso agregado exitosamente')
        return redirect(url_for('dashboard'))
    
    return render_template('nuevo_recurso.html')

@app.route('/estudiantes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_estudiante():
    if not session.get('es_admin'):
        flash('No tiene permisos para esta acción')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        matricula = request.form['matricula']
        email = request.form['email']
        
        if Estudiante.query.filter_by(matricula=matricula).first():
            flash('Ya existe un estudiante con esa matrícula')
            return render_template('nuevo_estudiante.html')
        
        nuevo = Estudiante(nombre=nombre, matricula=matricula, email=email)
        db.session.add(nuevo)
        db.session.commit()
        flash('Estudiante registrado exitosamente')
        return redirect(url_for('dashboard'))
    
    return render_template('nuevo_estudiante.html')

@app.route('/prestamos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_prestamo():
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        recurso_id = request.form['recurso_id']
        
        recurso = Recurso.query.get(recurso_id)
        if not recurso.disponible:
            flash('El recurso no está disponible')
            return redirect(url_for('nuevo_prestamo'))
        
        prestamo = Prestamo(estudiante_id=estudiante_id, recurso_id=recurso_id)
        recurso.disponible = False
        db.session.add(prestamo)
        db.session.commit()
        flash('Préstamo registrado exitosamente')
        return redirect(url_for('dashboard'))
    
    estudiantes = Estudiante.query.all()
    recursos = Recurso.query.filter_by(disponible=True).all()
    return render_template('nuevo_prestamo.html', 
                         estudiantes=estudiantes, 
                         recursos=recursos)

@app.route('/prestamos/devolver/<int:prestamo_id>')
@login_required
def devolver_prestamo(prestamo_id):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    if prestamo.estado != 'activo':
        flash('Este préstamo ya fue devuelto')
        return redirect(url_for('dashboard'))
    
    prestamo.estado = 'devuelto'
    prestamo.recurso.disponible = True
    db.session.commit()
    flash('Recurso devuelto exitosamente')
    return redirect(url_for('dashboard'))

@app.route('/estudiantes/<int:estudiante_id>/prestamos')
@login_required
def prestamos_estudiante(estudiante_id):
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    return render_template('prestamos_estudiante.html', estudiante=estudiante)

@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    flash('Has cerrado sesión exitosamente')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
