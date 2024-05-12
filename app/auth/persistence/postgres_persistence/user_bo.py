from typing import List

from app.auth.domain.bo.user_bo import UserBO
from app.auth.domain.persistence.auth_bo import AuthBOPersistenceInterface
from app.auth.models import User
from tortoise import transactions
from tortoise.exceptions import DoesNotExist

class AuthBOPostgresPersistenceService(AuthBOPersistenceInterface):

    @transactions.atomic()
    async def create_user(self, user: UserBO):
        print(f"Creating new User with username: {user.username}")  # Debugging
        new_user = await User.create(
            username=user.username,
            email=user.email,
            password=user.password,
        )
        print(f"New User created with ID: {new_user.id}")  # Debugging
        user.id = new_user.id
        print(f"UserBO ID set to: {user.id}")  # Debugging
        return user
    
    
    async def get_user_by_username(self, username: str):
        user_record = await User.filter(username=username).first()
        if user_record:
            return UserBO(
                id=user_record.id,
                username=user_record.username,
                email=user_record.email,
                password=user_record.password,
                auth_token=user_record.auth_token
            )
        return None

    async def invalidate_user_token(self, token: str):
        user_record = await User.filter(auth_token=token).first()
        if user_record:
            user_record.auth_token = None
            await user_record.save()
            return True
        return False

    async def get_user_by_token(self, token: str):
        user_record = await User.filter(auth_token=token).first()
        if user_record:
            return UserBO(
                id=user_record.id,
                username=user_record.username,
                password=user_record.password,
                email=user_record.email,
                auth_token=user_record.auth_token
            )
        return None
    
    async def update_user_auth_token(self, user_id, new_token):
        user_record = await User.get(id=user_id)
        if user_record:
            user_record.auth_token = new_token
            await user_record.save()
            return True
        return False