from typing import List
from app.auth.domain.bo.user_bo import UserBO
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from app.auth.models import User
from tortoise import transactions
from tortoise.exceptions import DoesNotExist
import redis


class AuthBOPostgresPersistenceService(AuthBOPersistenceInterface):
    def __init__(self):
        self.redis_client = redis_client = redis.Redis(
            host="redis", port=6379, decode_responses=True
        )
        self.token_ttl = 24 * 60 * 60

    @transactions.atomic()
    async def create_user(self, user: UserBO):
        print(
            f"Generating a new user with the chosen username: {user.username}"
        )  # Debugging
        new_user = await User.create(
            username=user.username,
            email=user.email,
            password=user.password,
        )
        print(
            f"A new user has been successfully created with the assigned ID.: {new_user.id}"
        )  # Debugging
        user.id = new_user.id
        print(f"UserBO ID: {user.id}")
        return user

    async def get_user_by_username(self, username: str):
        user_record = await User.filter(username=username).first()
        if user_record:
            token = self.redis_client.get(f"auth_token:{user_record.id}")
            return UserBO(
                id=user_record.id,
                username=user_record.username,
                email=user_record.email,
                password=user_record.password,
                auth_token=token,
            )
        return None

    async def invalidate_user_token(self, token: str):
        user_id = self.redis_client.get(f"token_to_user:{token}")
        if user_id:
            self.redis_client.delete(f"token_to_user:{token}")
            self.redis_client.delete(f"auth_token:{user_id}")
            return True
        return False

    async def get_user_by_token(self, token: str):
        user_id = self.redis_client.get(f"token_to_user:{token}")
        if user_id:
            # Fetch user from PostgreSQL
            user_record = await User.get(id=user_id)
            if user_record:
                return UserBO(
                    id=user_record.id,
                    username=user_record.username,
                    password=user_record.password,
                    email=user_record.email,
                    auth_token=token,
                )
        return None

    async def update_user_auth_token(self, user_id, new_token):
        try:
            user_record = await User.get(id=user_id)
            self.redis_client.setex(f"auth_token:{user_id}", self.token_ttl, new_token)
            self.redis_client.setex(
                f"token_to_user:{new_token}", self.token_ttl, user_id
            )
            return True
        except DoesNotExist:
            return False

    def __del__(self):
        self.redis_client.close()
