from fastapi import APIRouter, Body
from hashlib import sha256

router = APIRouter()

@router.delete("/{id}")
async def test2(id: int) -> dict[str, int]:
    return {"id": id}

users = {}

@router.post("/register")
async def register_func(input: dict = Body()):
    user = input["user"]
    password = input["pass"]
    print(user)
    print(password)
    hash_password = user + password
    users[user] = sha256(hash_password.encode()).digest()
    return {}

@router.post("/login")
async def login_func(input: dict = Body()):
    user = input["user"]
    password = sha256((user + input["pass"]).encode()).digest()
    print(user)
    print(password)
    print(password == users[user])
    token = generate_random()
    return {}