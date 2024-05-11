from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_bo import FileBOPersistences
from app.files.domain.controllers.files.crud.get_id import GetFileDomain


class FilesGetControllers(containers.DeclarativeContainer):
    v1 = providers.Singleton(
        GetFileDomain,
        FileBOPersistences.carlemany(),
    )

