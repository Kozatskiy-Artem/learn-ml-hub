from dependency_injector import containers, providers

from classification.repositories import ImageRepository
from classification.services import ClassificationService
from users.repositories import UserRepository
from users.services import UserService


class RepositoryContainer(containers.DeclarativeContainer):
    """
    A container responsible for providing instances of various repository classes.
    Repositories are data access components used by services to retrieve data.
    """

    image_repository = providers.Factory(ImageRepository)
    user_repository = providers.Factory(UserRepository)


class ServiceContainer(containers.DeclarativeContainer):
    """
    A container responsible for providing instances of various service classes.
    Services are responsible for interaction with the data storage layer and business logic of the application.
    """

    classification_service = providers.Factory(
        ClassificationService, image_repository=RepositoryContainer.image_repository
    )
    user_service = providers.Factory(UserService, user_repository=RepositoryContainer.user_repository)
