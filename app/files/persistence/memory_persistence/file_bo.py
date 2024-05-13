from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistence.file_bo import FileBOPersistenceInterface

files = {}


class FileBOMemoryPersistenceService(FileBOPersistenceInterface):

    async def create_file(self, file: FileBO):
        new_id = len(files)
        while new_id in files.keys():
            print(new_id)
            new_id += 1
        files[new_id] = file
        print(files)
        return new_id

    async def get_file(self, file_id: int):
        if file_id in files:
            file_to_return = files[file_id]
            return FileBO(
                id=file_to_return.id,
                name=file_to_return.name,
                description=file_to_return.description,
                content=file_to_return.content,
                user_id=file_to_return.user_id
            )
