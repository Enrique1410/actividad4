from abc import ABC, abstractmethod
from typing import List

from app.auth.domain.bo.user_bo import UserBO



class AuthBOPersistenceInterface(ABC):

    @abstractmethod
    async def create_user(self, user: UserBO):
        pass
    
    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    async def invalidate_user_token(self, token: str):
        pass

    @abstractmethod
    async def get_user_by_token(self, token: str):
        pass