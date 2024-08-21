from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# Importamos el modulo de Authenticacion de fastApi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordRequestForm : Mecanismo para capturar el email y la constraseña en este caso
# OAuth2PasswordBearer: Seria el sistema de Authentication

router = APIRouter()

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



# Operacion de consulta para saber si nuestro usuario esta en nuestra base de datos
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #realizamos la busqueda en la base de datos con la clave "username", utilizamos los doble ** para que la clase UserDB pueda recibir varios parametros

# Operacion de consulta para devolver el Usuario en concreto y no el UserDB (para no devolverle la password)
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Criterio de dependecia "Depends"
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales de Authenticacion invalidas",
            headers={"WWW-Authenticate": "Bearer"}) # añadimos cabeceras con el headers
   
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Usuario inactivo")
   
    return user        


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):  #lo importante es que sea de tipo Form, para envio de formulario. El Depends 
# Depends va a depender si el usuario esta autorizado o no para poder hacer las consultas.
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "El usuario no es correcto")

    user = search_user_db(form.username) #buscamos el usuario con la funcion de busqueda que creamos
    if not form.password == user.password:  #comprobamos si la contraseña que nos llego coincide con el usuario de la base de datos
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "La contraseña no es correcta")

    return {"access_token": user.username , "token_type": "bearer"} #retornamos el access token si el usuario existe    

#creamos una consulta que pida authentication, para eso utiliza DEPENDS
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user