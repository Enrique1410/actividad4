from app.files.domain.controllers.files.crud.delete import DeleteFileDomain
from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_bo import FileBOPersistences



class DeleteFileByFileIdController(containers.DeclarativeContainer):
     v1_get_by_token = providers.Singleton(
        DeleteFileDomain,
        FileBOPersistences.carlemany(),
    )
