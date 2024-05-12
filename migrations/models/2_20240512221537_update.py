from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "password" TYPE VARCHAR(300) USING "password"::VARCHAR(300);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "password" TYPE VARCHAR(50) USING "password"::VARCHAR(50);"""
