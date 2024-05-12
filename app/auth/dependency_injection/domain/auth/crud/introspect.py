
from app.auth.dependency_injection.domain.persistences.auth_bo import AuthBOPersistences
from app.auth.domain.controllers.auth.crud.introspect import InfoUser
from dependency_injector import containers, providers



class InfoUserControllers(containers.DeclarativeContainer):
     v1_info_user = providers.Singleton(
        InfoUser,
        AuthBOPersistences.carlemany(),
    )
