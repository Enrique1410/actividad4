from http.client import HTTPException
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface


class LogoutUser:
    def __init__(self, auth_persistence_service: AuthBOPersistenceInterface):
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, token: str):
        if await self.auth_persistence_service.invalidate_user_token(token):
            return {"message": "Logout successful"}
        else:
            raise HTTPException(status_code=404, detail="User not found")