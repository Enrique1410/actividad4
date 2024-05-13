from app.files.dependency_injection.domain.files.crud.delete import DeleteFileByFileIdController
from app.files.dependency_injection.domain.files.crud.get import FilesGetByTokenControllers
from fastapi import APIRouter, HTTPException, UploadFile, File, Header, Body, Path
from pydantic import BaseModel
from typing import Optional, Union, List, Dict
from pypdf import PdfMerger

from app.files.dependency_injection.domain.files.crud.get_id import FilesGetControllers
from app.files.dependency_injection.domain.files.crud.post import FilesPostControllers
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.controllers.files.crud.post import PostFileDomain

router = APIRouter()


files = {}

class File(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    content: Optional[str] = None
    user_id: Optional[int] = None

    model_config = {
        "json_schema_extra" :  {
            "examples": [
                {
                    "name": "File1",
                    "description": "Description file 1",
                    "content": "Content file 1",

                },
                {
                    "name": "File2",
                    "description": "Description file 2",
                }
            ]
        }
    }

@router.get("/")
async def get_files_by_token(token: str = Header(alias="user_token")) -> List[File]:
    get_files_controller = FilesGetByTokenControllers.v1_get_by_token()
    files_list = await get_files_controller(token_id=token)
    return files_list


@router.get("/{id}")
async def get_file(id: int, token: str = Header(alias="user_token")) -> File:
    get_files_controller = FilesGetControllers.v1()
    file_bo = await get_files_controller(input_file_id=id, token=token)
    return File(
        id=file_bo.id,
        name=file_bo.name,
        description=file_bo.description,
        content=file_bo.content,
        user_id=file_bo.user_id
    )


@router.post("/")
async def post_files(input_post_file: File, token: str = Header(alias="user_token")) -> File:

    post_files_controller = FilesPostControllers.v1_create_file()
    file_bo = FileBO(
        name=input_post_file.name,
        description=input_post_file.description,
        content=input_post_file.content,
    )
    file_to_return = await post_files_controller(token=token,input_post_file=file_bo)
    return  File(
        id=file_to_return.id,
        name=file_to_return.name,
        description=file_to_return.description,
        content=file_to_return.content,
        user_id=file_to_return.user_id
    )
    


@router.post("/merge")
async def post_merge() -> dict:
    file1 = "files/test1"
    file2 = "files/auth"
    merged = "files/merged"
    pdfs = [file1, file2]
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    name = merged
    merger.write(name)
    merger.close()

    new_id = len(files)
    while new_id in files.keys():
        print(new_id)
        new_id += 1
    files[new_id] = File(
        name="merged",
        author="carlemany_backend"
    )
    return {
        "id": new_id
    }


@router.post("/{id}")
async def post_files(id: int, any_name: str = Header(alias="AnyName"), input_post_files: File = Body()) -> dict[str, Union[int, Dict]]:
    print(any_name)
    if id not in files:
        raise HTTPException(
            status_code=411,
            detail="This file is not in the database"
        )
    files[id] = input_post_files
    return {}


#@router.post("/content/{id}")
#async def post_files(id: int, input_post_files: UploadFile = File()) -> dict[str, Union[int, Dict]]:
#    filename = "test"
#    prefix = "files/"
#    with open(prefix + filename, "wb") as buffer:
#       while chunk := await input_post_files.read(8192):
#           buffer.write(chunk)
#
#    if id not in files:
#        raise HTTPException(
#            status_code=411,
#            detail="This file is not in the database"
#        )
#    files[id] = input_post_files
#    return {}


@router.delete("/{id}")
async def delete_file(file_id: int):
    file_delete =  DeleteFileByFileIdController.v1_get_by_token()
    deleted_file = await file_delete(file_id)
    return {"status": "success", "message": deleted_file["message"]}
