from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

# Importamos el modulo de Authenticacion de fastApi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordRequestForm : Mecanismo para capturar el email y la constraseña en este caso
# OAuth2PasswordBearer: Seria el sistema de Authentication


app = FastAPI()

# Criterio de Authentication 
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entidad User
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

# Entidad UserDB
class UserDB(User):
    password: str  


# Datos Ficticios de mi base de datos    
users_db = {
    "nicolasViruel":{
        "username": "Nicolas",
        "fullname": "Viruel", 
        "email": "nicolas@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "nicolasViruel2":{
        "username": "Nicolas2",
        "fullname": "Viruel2", 
        "email": "nicolas2@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}       