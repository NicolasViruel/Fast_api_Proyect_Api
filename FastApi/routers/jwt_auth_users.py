from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

# Importamos el modulo de Authenticacion de fastApi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordRequestForm : Mecanismo para capturar el email y la constraseña en este caso
# OAuth2PasswordBearer: Seria el sistema de Authentication

# Importamos jwt
from jose import jwt
# Importamos el Crytp
from passlib.context import CryptContext

# Algoritmo de Hash
ALGORITHM = "HS256"

app = FastAPI()

# Criterio de Authentication 
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Contexto de encriptacion

crypt = CryptContext(schemes=["bcrypt"])

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


# Operacion de consulta para saber si nuestro usuario esta en nuestra base de datos
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #realizamos la busqueda en la base de datos con la clave "username", utilizamos los doble ** para que la clase UserDB pueda recibir varios parametros




@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):  #lo importante es que sea de tipo Form, para envio de formulario. El Depends 
# Depends va a depender si el usuario esta autorizado o no para poder hacer las consultas.
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "El usuario no es correcto")

    user = search_user_db(form.username) #buscamos el usuario con la funcion de busqueda que creamos
    if not form.password == user.password:  #comprobamos si la contraseña que nos llego coincide con el usuario de la base de datos
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "La contraseña no es correcta")

    return {"access_token": user.username , "token_type": "bearer"} #retornamos el access token si el usuario existe    
