from fastapi import APIRouter


# Inicio del servidor uvicorn products:app --reload
router = APIRouter(prefix="/products", tags=["products"], responses={404: {"message": "No encontrado"}} ) 
#prefix te fija la URY del router para no tener que estar poniendo a cada ruta
#response: Es la respuesta que queremos darle
#Tags: Es el prefijo para que aparezca en la documentacion

products_list = ["producto 1", "producto 2", "producto 3", "producto 4" ]



@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]    