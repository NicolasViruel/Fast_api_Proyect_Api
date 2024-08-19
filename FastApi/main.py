from fastapi import FastAPI

# Importo el Router
from routers import products, users

# Importo la clase staticFile para los archivos estaticos
from fastapi.staticfiles import StaticFiles




app = FastAPI()

# Routers
app.include_router(products.router) 
app.include_router(users.router) 

# Montar recursos estaticos ()
app.mount("/static", StaticFiles(directory="static"), name="static")



# Inicio del servidor uvicorn main:app --reload
@app.get("/")
async def root():
    return {"message": "Fast Api"}