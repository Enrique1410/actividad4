from app.auth.dependency_injection.domain.persistences.auth_bo import AuthBOPersistences
from app.auth.domain.controllers.auth.crud.register import RegisterUser
from dependency_injector import containers, providers



class RegisterUserControllers(containers.DeclarativeContainer):
     v1_create_user = providers.Singleton(
        RegisterUser,
        AuthBOPersistences.carlemany(),
    )
