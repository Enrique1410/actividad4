from app.auth.domain.bo.user_bo import UserBO
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from hashlib import sha256


class RegisterUser:
    def __init__(self, auth_persistence_service: AuthBOPersistenceInterface):
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, user: UserBO):
        if await self.auth_persistence_service.exists(user.username):
            raise ValueError("User already exists")

        hashed_password = sha256((user.username + user.password).encode()).digest()
        user.password = hashed_password
        await self.user_repository.save(user)
        return user