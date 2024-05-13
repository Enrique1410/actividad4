from fastapi import HTTPException
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface


class GetFileDomain:
    def __init__(self, file_persistence_service: FileBOPersistenceInterface, auth_persistence_service: AuthBOPersistenceInterface):
        self.file_persistence_service = file_persistence_service
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, token: str, input_file_id: int) -> FileBO:
        user = await self.auth_persistence_service.get_user_by_token(token)
        if not user:
            raise HTTPException(status_code=404, detail="Invalid token or user not found")
        print(user)
        file_to_return = await self.file_persistence_service.get_file(file_id=input_file_id)
        file_to_return.user_id = user.id
        print(file_to_return)
        if not file_to_return or file_to_return.user_id != user.id:
            raise HTTPException(status_code=404, detail="File not found or access denied")

        return file_to_return
