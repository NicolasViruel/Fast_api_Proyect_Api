from fastapi import APIRouter, HTTPException # HTTPException para darles avisos en las request http como los status

# Pydantic es la BaseModel del modelo
from pydantic import BaseModel


# Inicio del servidor uvicorn users:app --reload
router = APIRouter(prefix="/usersdb", tags=["usersdb"], responses={404: {"message": "No encontrado"}} ) 

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Datos Ficticios de mi base de datos
users_list = [User(id=1, name="Nicolas", surname="Viruel", url="hhttps://mourde.dev", age=35),
              User(id=2, name="Alejandro", surname="Viruel", url="hhttps://mourde.dev", age=38),
              User(id=3, name="Catalina", surname="Viruel", url="hhttps://mourde.dev", age=2)]   



@router.get("/")
async def users():
    return users_list

# Get Users por Id // ---- Traer datos por el Path -----
@router.get("/{id}")
async def user(id: int):
    return search_user(id)


# Get Users por Id // ---- Traer datos por Query -----
@router.get("/")
async def user(id: int):
    search_user(user.id)
    return search_user(id)


# Post Añadir usuario
#response_model es lo que responde en caso que valla bien

@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    #Buscamos si es del tipo User y sino lo añadimos
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail= "El usuario ya existe")
       
    else:
        users_list.append(user)
        return user


# Put Modificar usuario

@router.put("/")
async def user(user: User):
    found = False

    #recorremos la lista y si consiste el id lo reemplazamos
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            #si lo encontramos accedemos a la lista justo en su indice y lo mandamos
            users_list[index] = user
            found = True
            break # Salimos del bucle porque ya encontramos y actualizamos el usuario

        # Si no lo encontramos devolvemos el error        
    if not found:
        return {"error":"No se ha actualizado el usuario"}        
                
    return user 


# Delete usuario

@router.delete("/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            #si lo encontramos accedemos a su indice y lo eliminamos
            del users_list[index]
            found = True
            break # Salimos del bucle porque ya encontramos y actualizamos el usuario
            return "El usuario ha sido Eliminado"
            # Si no lo encontramos devolvemos el error        
    if not found:
        return {"error":"No se ha actualizado el usuario"}




# ------------------- ///////// Podemos definir una funcion que realize la consulta  ///////// ------------------- 
def search_user(id: int):
 #filtramos un usuario de la lista por el id, con el metodo filter
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}



