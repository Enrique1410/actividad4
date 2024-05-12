from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL,
    "password" VARCHAR(50) NOT NULL,
    "auth_token" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "files" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(50) NOT NULL,
    "content" VARCHAR(50) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
