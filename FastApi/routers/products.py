from fastapi import APIRouter


# Inicio del servidor uvicorn users:app --reload
router = APIRouter(prefix="/products") #prefix te fija la URY del router para no tener que estar poniendo a cada ruta


products_list = ["producto 1", "producto 2", "producto 3", "producto 4" ]



@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]    