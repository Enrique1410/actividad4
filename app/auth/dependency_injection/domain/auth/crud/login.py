from app.auth.dependency_injection.domain.persistences.auth_bo import AuthBOPersistences
from app.auth.domain.controllers.auth.crud.login import LoginUser
from dependency_injector import containers, providers



class LoginUserControllers(containers.DeclarativeContainer):
     v1_login_user = providers.Singleton(
        LoginUser,
        AuthBOPersistences.carlemany(),
    )
