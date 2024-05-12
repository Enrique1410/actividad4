from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface
from typing import List

class GetFilesByTokenDomain:

    def __init__(self, file_persistence_service: FileBOPersistenceInterface, auth_persistence_service: AuthBOPersistenceInterface):
        self.file_persistence_service = file_persistence_service
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, token_id: str) -> List[FileBO]:
        user = await self.auth_persistence_service.get_user_by_token(token_id)
        if not user:
            raise ValueError("Invalid token or user not found") 

        files_to_return = await self.file_persistence_service.get_files_by_user_id(user.id)
        return files_to_return
