from fastapi import FastAPI

app = FastAPI()

# Inicio del servidor uvicorn main:app --reload
@app.get("/")
async def root():
    return {"message": "Fast Api"}