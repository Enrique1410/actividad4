from fastapi import APIRouter, HTTPException, UploadFile, File as FastAPIFile, Header
from typing import List
from app.files.dependency_injection.domain.files.crud.get import (
    FilesGetByTokenControllers,
)
from app.files.dependency_injection.domain.files.crud.get_id import FilesGetControllers
from app.files.dependency_injection.domain.files.crud.post import FilesPostControllers
from app.files.dependency_injection.domain.files.crud.delete import (
    DeleteFileByFileIdController,
)
from app.files.domain.bo.file_bo import FileBO
import os

router = APIRouter()


@router.get("/", response_model=List[FileBO])
async def get_files_by_token(token: str = Header(alias="user_token")):
    get_files_controller = FilesGetByTokenControllers.v1_get_by_token()
    files_list = await get_files_controller(token_id=token)
    return files_list


@router.get("/{id}", response_model=FileBO)
async def get_file(id: int, token: str = Header(alias="user_token")):
    get_files_controller = FilesGetControllers.v1()
    file_bo = await get_files_controller(input_file_id=id, token=token)
    return file_bo


@router.post("/", response_model=FileBO)
async def post_files(
    file: UploadFile = FastAPIFile(...),
    description: str = None,
    token: str = Header(alias="user_token"),
):
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    file_bo = FileBO(
        name=file.filename,
        description=description,
        content=temp_path,  # Pass file path to MinIO service
    )
    post_files_controller = FilesPostControllers.v1_create_file()
    file_to_return = await post_files_controller(token=token, input_post_file=file_bo)

    # Clean up
    os.remove(temp_path)
    return file_to_return


@router.delete("/{id}")
async def delete_file(file_id: int):
    file_delete = DeleteFileByFileIdController.v1_get_by_token()
    deleted_file = await file_delete(file_id)
    return deleted_file


# Remove /merge and /{id} POST endpoints unless you need them for something else
