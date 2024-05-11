from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface


class PostFileDomain:

    def __init__(self, file_persistence_service: FileBOPersistenceInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, input_post_file: FileBO):
        new_id = await self.file_persistence_service.create_file(file=input_post_file)
        return new_id
