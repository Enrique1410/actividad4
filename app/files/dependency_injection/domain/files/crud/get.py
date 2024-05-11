
from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_bo import FileBOPersistences
from app.files.domain.controllers.files.crud.get import GetFilesByTokenDomain


class FilesGetByTokenControllers(containers.DeclarativeContainer):
     v1_get_by_token = providers.Singleton(
        GetFilesByTokenDomain,
        FileBOPersistences.carlemany(),
    )

