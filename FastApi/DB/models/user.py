# Pydantic es la BaseModel del modelo
from pydantic import BaseModel


# Entidad User
class User(BaseModel):
    id: int
    username: str
    email: str