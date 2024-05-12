from app.auth.persistence.postgres_persistence.user_bo import AuthBOPostgresPersistenceService
from dependency_injector import containers, providers



class AuthBOPersistences(containers.DeclarativeContainer):
    postgres = providers.Singleton(
        AuthBOPostgresPersistenceService
    )

    #memory = providers.Singleton(
    #    AuthBOMemoryPersistenceService
    #)

    carlemany = postgres