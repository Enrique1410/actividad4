from dependency_injector import containers, providers

from app.files.persistence.memory_persistence.file_bo import FileBOMemoryPersistenceService
from app.files.persistence.postgres_persistence.file_bo import FileBOPostgresPersistenceService


class FileBOPersistences(containers.DeclarativeContainer):
    postgres = providers.Singleton(
        FileBOPostgresPersistenceService
    )

    memory = providers.Singleton(
        FileBOMemoryPersistenceService
    )

    carlemany = postgres
