from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.files.api.router import router as files_router
from app.auth.api.router import router as auth_router
from app.config import DATABASE_URL, models


tags_metadata = [
    {
        "name": "files",
        "description": "desc files"
    },
    {
        "name": "auth",
        "description": "desc auth"
    }
]

app = FastAPI(
    title="Actividad III Grupo 7",
    description="Actividad III Grupo 7",
    tags_metadata=tags_metadata
)

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(files_router, prefix="/files", tags=["files"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": models},
    generate_schemas=False,
    add_exception_handlers=True,
)
