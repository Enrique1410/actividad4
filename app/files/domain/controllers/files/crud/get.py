from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface
from typing import List

class GetFilesByTokenDomain:

    def __init__(self, file_persistence_service: FileBOPersistenceInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, token_id: str) -> List[FileBO]:
        files_to_return = await self.file_persistence_service.get_files_by_token(token_id=token_id)
        return files_to_return
