import base64
from fastapi import HTTPException
import secrets
from app.auth.domain.bo.user_bo import UserBO
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from hashlib import sha256


class LoginUser:
    def __init__(self, auth_persistence_service: AuthBOPersistenceInterface):
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, username: str, password: str):
        user_bo = await self.auth_persistence_service.get_user_by_username(username)
        if not user_bo:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        hashed_password = sha256((username + password).encode()).digest()
        base64_encoded_password = base64.b64encode(hashed_password).decode('utf-8')
        if base64_encoded_password != user_bo.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        new_token = secrets.token_hex(16)
        success = await self.auth_persistence_service.update_user_auth_token(user_bo.id, new_token)
        if success:
            return {"message": "Login successful", "token": new_token}
        else:
            raise HTTPException(status_code=500, detail="Failed to update user token")

            
