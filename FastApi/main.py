from fastapi import FastAPI

# Importo el Router
from routers import products, users




app = FastAPI()

# Routers
app.include_router(products.router) 
app.include_router(users.router) 

# Inicio del servidor uvicorn main:app --reload
@app.get("/")
async def root():
    return {"message": "Fast Api"}