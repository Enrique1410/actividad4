from typing import List
from minio import Minio
from minio.error import S3Error
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface
from app.files.models import File
from tortoise import transactions
from tortoise.exceptions import DoesNotExist
import os


class MinioFileBOPersistenceService(FileBOPersistenceInterface):
    def __init__(self):
        self.minio_client = Minio(
            "minio-server:9000", access_key="minio", secret_key="minio123", secure=False
        )
        self.bucket_name = "backend-carlemany-s3-bucket"

    @transactions.atomic()
    async def create_file(self, file: FileBO) -> FileBO:
        # Assuming file.content is the local file path for upload (updated in controller)
        if not file.content or not os.path.exists(file.content):
            raise ValueError("File content path is invalid")

        object_name = f"users/{file.user_id}/{os.path.basename(file.name)}"
        try:
            self.minio_client.fput_object(self.bucket_name, object_name, file.content)
            new_file = await File.create(
                name=file.name,
                description=file.description,
                object_name=object_name,
                user_id=file.user_id,
            )
            return FileBO(
                id=new_file.id,
                name=new_file.name,
                description=new_file.description,
                content=None,  # Content isn’t stored locally anymore
                user_id=new_file.user_id,
            )
        except S3Error as e:
            raise Exception(f"Failed to upload file to MinIO: {e}")

    async def get_file(self, file_id: int) -> FileBO:
        try:
            file = await File.get(id=file_id)
            url = f"http://minio-server:9000/{self.bucket_name}/{file.object_name}"
            return FileBO(
                id=file.id,
                name=file.name,
                description=file.description,
                content=url,  # Return URL instead of content
                user_id=file.user_id,
            )
        except DoesNotExist:
            return None  # Handled by controllers

    async def get_files_by_user_id(self, user_id: int) -> List[FileBO]:
        files = await File.filter(user_id=user_id).all()
        return [
            FileBO(
                id=file.id,
                name=file.name,
                description=file.description,
                content=f"http://minio-server:9000/{self.bucket_name}/{file.object_name}",
                user_id=file.user_id,
            )
            for file in files
        ]

    async def delete_file(self, file_id: int) -> dict:
        try:
            file = await File.get(id=file_id)
            object_name = file.object_name
            self.minio_client.remove_object(self.bucket_name, object_name)
            file_info = f"id {file_id}, Name {file.name}"
            await file.delete()
            return {
                "status": "success",
                "message": f"File {file_info} successfully deleted",
            }
        except DoesNotExist:
            return {"status": "error", "message": f"File id {file_id} not found"}
        except S3Error as e:
            raise Exception(f"Failed to delete file from MinIO: {e}")
