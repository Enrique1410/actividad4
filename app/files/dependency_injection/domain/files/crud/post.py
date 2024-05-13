from app.auth.dependency_injection.domain.persistences.auth_bo import AuthBOPersistences
from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_bo import FileBOPersistences
from app.files.domain.controllers.files.crud.post import PostFileDomain


class FilesPostControllers(containers.DeclarativeContainer):
    v1_create_file = providers.Singleton(
        PostFileDomain,
        file_persistence_service=FileBOPersistences.carlemany(),
        auth_persistence_service=AuthBOPersistences.carlemany()
    )

