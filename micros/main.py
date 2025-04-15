from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import requests

app = FastAPI()

class TipoUsuario(str, Enum):
    ADMIN = "admin"
    USER = "user"
    TEACHER = "teacher"

class Usuario(BaseModel):
    id: int
    nombre: str
    tipo: TipoUsuario
    state: bool

usuarios = [
    Usuario(id=1, nombre="Admin", tipo=TipoUsuario.ADMIN, state=True),
    Usuario(id=2, nombre="Teacher", tipo=TipoUsuario.TEACHER, state=True),
    Usuario(id=3, nombre="User", tipo=TipoUsuario.USER, state=False)
]

@app.get("/probar")
def probar_mockoon():
    response = requests.get("http://localhost:8000/test")
    return response.json()

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a mi microservicio"}

@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    return {"error": "Usuario no encontrado"}

@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

@app.get("/usuarios/tipo/{tipo}")
def obtener_usuario_por_tipo(tipo: TipoUsuario):
    usuarios_filtrados = [u for u in usuarios if u.tipo == tipo]
    return usuarios_filtrados

@app.post("/usuario")
def crear_usuario(usuario: Usuario):
    
    if usuario.tipo == TipoUsuario.ADMIN:
        usuario.id = 1
        usuario.state = True
    elif usuario.tipo == TipoUsuario.TEACHER:
        usuario.id = 2
        usuario.state = True
    elif usuario.tipo == TipoUsuario.USER:
        usuario.id = 3
        usuario.state = False
    
    for i, u in enumerate(usuarios):
        if u.id == usuario.id:
            usuarios[i] = usuario
            return {"mensaje": "Usuario actualizado", "usuario": usuario}
    
    usuarios.append(usuario)
    return {"mensaje": "Usuario creado", "usuario": usuario}
