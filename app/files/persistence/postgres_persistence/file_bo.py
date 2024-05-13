from typing import List
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface

from app.files.models import File
from tortoise import transactions
from tortoise.exceptions import DoesNotExist

class FileBOPostgresPersistenceService(FileBOPersistenceInterface):

    @transactions.atomic()
    async def create_file(self, file: FileBO):
        new_file = await File.create(
            name=file.name,
            description=file.description,
            content=file.content,
            user_id=file.user_id
        )
        file.id = new_file.id
    
        return FileBO(
            id=file.id,
            name=file.name,
            description=file.description,
            content=file.content,
            user_id=file.user_id
        )

    async def get_file(self, file_id: int,) -> FileBO:
        file = await File.get(
            id=file_id
        )
        return FileBO(
            id=file.id,
            name=file.name,
            description=file.description,
            content=file.content,
        )
    
    async def get_files_by_user_id(self, user_id: int) -> List[FileBO]:
        files = await File.filter(user_id=user_id).all()
        return [
        FileBO(
            id=file.id,
            name=file.name,
            description=file.description,
            content=file.content
        ) for file in files
    ]

    async def delete_file(self, file_id: int):
        try:
            file = await File.get(id=file_id)
            file_info = f"id {file_id}, Name {file.name}"
            await file.delete()
            return {"status": "success", "message": f"File {file_info} successfully deleted"}
        except DoesNotExist:
            return {"status": "error", "message": f"File {file_info} not found"}
    
    async def update_file_content(self, file_id: int, token_id: str, new_content: str):
        try:
            file = await File.get(id=file_id, token_id=token_id)
            file.content = new_content
            await file.save()
            return {"status": "success", "message": "File content updated successfully"}
        except DoesNotExist:
            return {"status": "error", "message": "File not found or access denied"}

