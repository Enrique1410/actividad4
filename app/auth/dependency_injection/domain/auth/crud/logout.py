from app.auth.dependency_injection.domain.persistences.auth_bo import AuthBOPersistences
from app.auth.domain.controllers.auth.crud.logout import LogoutUser
from dependency_injector import containers, providers



class LogoutUserControllers(containers.DeclarativeContainer):
     v1_logout_user = providers.Singleton(
        LogoutUser,
        AuthBOPersistences.carlemany(),
    )
