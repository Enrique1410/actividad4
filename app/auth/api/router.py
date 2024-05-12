from hashlib import sha256
from app.auth.dependency_injection.domain.auth.crud.introspect import InfoUserControllers
from app.auth.dependency_injection.domain.auth.crud.login import LoginUserControllers
from app.auth.dependency_injection.domain.auth.crud.logout import LogoutUserControllers
from app.auth.dependency_injection.domain.auth.crud.register import RegisterUserControllers
from fastapi import APIRouter, HTTPException, UploadFile, File, Header, Body, Path
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    email: str
    password: str

    model_config = {
        "json_schema_extra" :  {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@johndoe.com",
                    "password": "johndoe",

                },
                {
                   "username": "janesmith",
                    "email": "janesmith@janesmith.com",
                    "password": "janesmith",
                }
            ]
        }
    }

@router.post("/register")
async def register(user: User):
    create_user_controller = RegisterUserControllers.v1_create_user()
    registered_user = await create_user_controller.execute(user)
    return {"message": "User registered successfully", "username": registered_user.username}


@router.post("/login")
async def login(username: str, password: str):
    user_login_controller = LoginUserControllers.v1_login_user()
    loged_user = await user_login_controller.execute(username, password)
    return loged_user


@router.post("/logout")
async def logout(token: str = Header(...)):
    logout_user_controller = LogoutUserControllers.v1_logout_user()
    loggedout_user = await logout_user_controller.execute(token)
    return loggedout_user

@router.get("/introspect")
async def introspect(token: str = Header(...)):
    info_user_controller = InfoUserControllers.v1_info_user()
    user_info = await info_user_controller.execute(token)
    return {"user": user_info}