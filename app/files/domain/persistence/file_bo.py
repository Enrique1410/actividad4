from abc import ABC, abstractmethod
from typing import List

from app.files.domain.bo.file_bo import FileBO


class FileBOPersistenceInterface(ABC):

    @abstractmethod
    async def create_file(self, file: FileBO):
        pass

    @abstractmethod
    async def get_file(self, file_id: int):
        pass

    @abstractmethod
    async def get_files_by_user_id(self, user_id: int) -> List[FileBO]:
        pass

    @abstractmethod
    async def delete_file(self, file_id: int):
        pass