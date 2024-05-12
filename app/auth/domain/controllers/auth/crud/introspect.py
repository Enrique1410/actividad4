from fastapi import HTTPException
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface


class InfoUser:
    def __init__(self, auth_persistence_service: AuthBOPersistenceInterface):
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, token: str):
        user = await self.auth_persistence_service.get_user_by_token(token)
        if not user:
            raise HTTPException(status_code=404, detail="Invalid token or user not found")
        return user