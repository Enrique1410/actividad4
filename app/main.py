import os
from fastapi import FastAPI, Header, File, UploadFile, Response
from fastapi.responses import FileResponse
from pypdf import PdfMerger
from typing import Any

from app.config import postgres_settings

app = FastAPI()

print(postgres_settings)

ids = []
mails = []
passwords = []
tokens = {}
file_names = {"test1": 0, "test2": 1}


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
async def login(input: dict) -> dict[str, str]:
    mail = input["mail"]
    password = input["password"]
    index = mails.index(mail)
    stored_password = passwords[index]
    if stored_password == password:
        new_token = "valid_token"
        tokens[mail] = new_token
        return {"token": new_token}
    return {"error": "true"}


@app.post("/register")
async def register(input: dict) -> dict[str, str]:
    mail = input["mail"]
    password = input["password"]
    ids.insert(0, len(ids))
    mails.insert(0, mail)
    passwords.insert(0, password)
    return {}


@app.post("/logout")
async def logout(header: str = Header(alias="Authorization")) -> dict[str, str]:
    input_token = header
    for mail, token in tokens.items():
        if input_token == token:
            del tokens["mail"]
            break
    return {}


@app.post("/introspect")
async def introspect(header: str = Header(alias="Authorization")) -> dict[str, str]:
    input_token = header
    for mail, token in tokens.items():
        if input_token == token:
            index = mails.index(mail)
            current_id = ids[index]
            password = passwords[index]
            return {"password": password, "id": current_id, "mail": mail}
    return {"error": "not found"}


@app.get("/file")
async def get_file() -> dict[str, Any]:
    files = []
    for name, id in file_names.items():
        files.append({"id": id, "name": name})
    return {"files": files}


@app.post("/file")
async def post_file(input: dict) -> dict[str, int]:
    id = len(file_names)
    name = input["name"]
    file_names[name] = id
    return {"id": id}


@app.get("/file/{id}")
async def get_file(id: int):
    for current_name, current_id in file_names.items():
        if current_id == id:
            filename = current_name
    return FileResponse(filename, media_type="application/pdf", filename=filename)


@app.post("/file/merge")
async def merge_files(input: dict) -> dict[str, int]:
    pdfs = []
    for current_name, current_id in file_names.items():
        if current_id in input["files"]:
            pdfs.append(current_name)
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    id = len(file_names)
    name = input["name"]
    merger.write(name)
    merger.close()
    file_names[name] = id
    return {"id": id}


@app.post("/file/{id}")
async def post_file(id: int, file: UploadFile = File()) -> dict[str, str]:
    for current_name, current_id in file_names.items():
        if current_id == id:
            filename = current_name
    with open(filename, "wb") as buffer:
        while chunk := await file.read(8192):
            buffer.write(chunk)
    return {}


@app.delete("/file/{id}")
async def delete_file(id: int) -> dict[str, str]:
    for current_name, current_id in file_names.items():
        if current_id == id:
            filename = current_name
    try:
        os.remove(filename)
    except Exception:
        pass
    del file_names[filename]
    return {}
