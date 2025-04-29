from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from .models import db, Usuario, Estudiante, Recurso, Prestamo

api = FastAPI(title="API Biblioteca Universitaria")

# Configuración JWT
SECRET_KEY = "your-secret-key-here"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str

class PrestamoCreate(BaseModel):
    estudiante_id: int
    recurso_id: int

class EstudianteCreate(BaseModel):
    nombre: str
    matricula: str
    email: str

class RecursoCreate(BaseModel):
    nombre: str
    tipo: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = Usuario.query.filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user

@api.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Usuario.query.filter_by(username=form_data.username).first()
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@api.post("/recursos/")
async def crear_recurso(recurso: RecursoCreate, current_user: Usuario = Depends(get_current_user)):
    if not current_user.es_admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    nuevo_recurso = Recurso(nombre=recurso.nombre, tipo=recurso.tipo)
    db.session.add(nuevo_recurso)
    db.session.commit()
    return {"id": nuevo_recurso.id, "mensaje": "Recurso creado exitosamente"}

@api.post("/estudiantes/")
async def crear_estudiante(estudiante: EstudianteCreate, current_user: Usuario = Depends(get_current_user)):
    if not current_user.es_admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    nuevo_estudiante = Estudiante(
        nombre=estudiante.nombre,
        matricula=estudiante.matricula,
        email=estudiante.email
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return {"id": nuevo_estudiante.id, "mensaje": "Estudiante registrado exitosamente"}

@api.post("/prestamos/")
async def crear_prestamo(prestamo: PrestamoCreate, current_user: Usuario = Depends(get_current_user)):
    recurso = Recurso.query.get_or_404(prestamo.recurso_id)
    if not recurso.disponible:
        raise HTTPException(status_code=400, detail="El recurso no está disponible")
    
    nuevo_prestamo = Prestamo(
        estudiante_id=prestamo.estudiante_id,
        recurso_id=prestamo.recurso_id
    )
    recurso.disponible = False
    db.session.add(nuevo_prestamo)
    db.session.commit()
    return {"id": nuevo_prestamo.id, "mensaje": "Préstamo registrado exitosamente"}

@api.get("/prestamos/estudiante/{estudiante_id}")
async def obtener_prestamos_estudiante(estudiante_id: int, current_user: Usuario = Depends(get_current_user)):
    prestamos = Prestamo.query.filter_by(estudiante_id=estudiante_id).all()
    return [{"id": p.id, "fecha_prestamo": p.fecha_prestamo, "estado": p.estado} for p in prestamos]

@api.put("/prestamos/{prestamo_id}/devolver")
async def devolver_prestamo(prestamo_id: int, current_user: Usuario = Depends(get_current_user)):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    if prestamo.estado != 'activo':
        raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")
    
    prestamo.estado = 'devuelto'
    prestamo.fecha_devolucion = datetime.utcnow()
    prestamo.recurso.disponible = True
    db.session.commit()
    return {"mensaje": "Recurso devuelto exitosamente"}
