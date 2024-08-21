from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta # timedelta es para el calculo de fechas

# Importamos el modulo de Authenticacion de fastApi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordRequestForm : Mecanismo para capturar el email y la constraseña en este caso
# OAuth2PasswordBearer: Seria el sistema de Authentication

# Importamos jwt
from jose import jwt, JWTError
# Importamos el Crytp
from passlib.context import CryptContext

# Algoritmo de Hash
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "asdqweqweqnkmkasmdlkm"  # Semilla

router = APIRouter()

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
        "password": "$2a$12$QTe75KVdgiDzTRw.5KjVM..HPS7NJRTmMvLTf/pqe4rCpq/hWG8kW"
    },
    "nicolasViruel2":{
        "username": "Nicolas2",
        "fullname": "Viruel2", 
        "email": "nicolas2@gmail.com",
        "disabled": True,
        "password": "$2a$12$9y7rwqkYlKUC.oDpu9kBPe7xPdxkC23pXDq/K0Iiqi4kyEQ5l0vX2"
    }
}


   


# Operacion de consulta para saber si nuestro usuario esta en nuestra base de datos
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) #realizamos la busqueda en la base de datos con la clave "username", utilizamos los doble ** para que la clase UserDB pueda recibir varios parametros

# Operacion de consulta para devolver el Usuario en concreto y no el UserDB (para no devolverle la password)
def search_user(username: str):
    user = None
    for user_data in users_db.values():
        if user_data["username"] == username:
            user = User(**user_data)
            break
    # print(f"Usuario encontrado en search_user: {user}")
    return user



# Buscamos el usuario authenticado
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de Autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise exception
        # print(f"Token decodificado correctamente, usuario: {username}")
    except JWTError as e:
        print(f"Error al decodificar el token: {str(e)}")
        raise exception

    user = search_user(username=username)
    if user is None:
        raise exception

    return user    
   

# Criterio de dependecia "Depends"
async def current_user(user: User = Depends(auth_user)):
    print(f"Usuario autenticado: {user.username}, Disabled: {user.disabled}")
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
   
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):  #lo importante es que sea de tipo Form, para envio de formulario. El Depends 
# Depends va a depender si el usuario esta autorizado o no para poder hacer las consultas.
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "El usuario no es correcto")

    user = search_user_db(form.username) #buscamos el usuario con la funcion de busqueda que creamos
    
    
    # Verificamos la contraseña
    
    if not crypt.verify(form.password, user.password): #comprobamos si la contraseña que nos llego coincide con el usuario de la base de datos
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "La contraseña no es correcta")

    # Creamos una access_token de forma segura

    access_token = { "sub": user.username,
                     "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION)    
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm= ALGORITHM) , "token_type": "bearer"} #retornamos el access token si el usuario existe    


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 