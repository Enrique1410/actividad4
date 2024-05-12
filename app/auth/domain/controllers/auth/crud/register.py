import base64
from app.auth.domain.bo.user_bo import UserBO
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from hashlib import sha256


class RegisterUser:
    def __init__(self, auth_persistence_service: AuthBOPersistenceInterface):
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, user: UserBO):
       

        hashed_password = sha256((user.username + user.password).encode()).digest()
        base64_encoded_password = base64.b64encode(hashed_password).decode('utf-8')
        user.password = base64_encoded_password
        saved_user = await self.auth_persistence_service.create_user(user)
        return saved_user