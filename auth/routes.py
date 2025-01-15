from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from .jwt_token import create_access_token

router = APIRouter()

class LoginData(BaseModel):
    username: str
    password: str

fake_user = {"username": "Gethin", "password": "admin"}

@router.post("/login")
async def login(data: LoginData):
    if data.username != fake_user["username"] or data.password != fake_user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = create_access_token(data={"sub": data.username})
    return {"access_token": access_token, "token_type": "bearer"}
