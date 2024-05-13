from fastapi import HTTPException
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface


class PostFileDomain:
    def __init__(self, file_persistence_service: FileBOPersistenceInterface, auth_persistence_service: AuthBOPersistenceInterface):
        self.file_persistence_service = file_persistence_service
        self.auth_persistence_service = auth_persistence_service

    async def __call__(self, token: str, input_post_file: FileBO):
        user = await self.auth_persistence_service.get_user_by_token(token)
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail="Invalid token or user not found")

        print(input_post_file.user_id)
        input_post_file.user_id = user.id
        print(input_post_file.user_id)
        file = await self.file_persistence_service.create_file(file=input_post_file)
        print(file)
        return file
