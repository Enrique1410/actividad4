from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.files.api.router import router as test_router
from app.auth.router import router as test2_router
from app.config import DATABASE_URL, models


tags_metadata = [
    {
        "name": "test1",
        "description": "desc test1"
    },
    {
        "name": "auth",
        "description": "desc test1"
    }
]

app = FastAPI(
    title="3d videoconference",
    description="Some description here",
    tags_metadata=tags_metadata
)

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(test_router, prefix="/books", tags=["books"])
app.include_router(test2_router, prefix="/auth", tags=["auth"])

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": models},
    generate_schemas=False,
    add_exception_handlers=True,
)
