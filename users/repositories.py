from annoying.functions import get_object_or_None

from core.exceptions import InstanceNotExistError

from .dto import UserDTO
from .interfaces import UserRepositoryInterface
from .models import UserModel


class UserRepository(UserRepositoryInterface):
    """
    A repository for managing user profile data in the application.

    This class implements UserRepositoryInterface and provides methods for working with user data in the database.

    Methods:

    - get_profile(user_id): Retrieve user profile information from the database.
    """

    def get_profile(self, user_id):
        """
        Retrieve user profile information.

        Args:
            user_id (int): The ID of the user.

        Returns:
            UserDTO - Data Transfer Object representing user profile.

        Raises:
            InstanceNotExistError: If the user with the given ID does not exist or is not active.
        """

        user = get_object_or_None(UserModel, id=user_id)
        if not user or not user.is_active:
            raise InstanceNotExistError(message=f"User with given id={user_id} does not exist error")

        return self._user_to_dto(user)

    @staticmethod
    def _user_to_dto(user: UserModel) -> UserDTO:
        """
        Convert a UserModel instance to a UserDTO.

        Args:
            user (UserModel): The user model instance.

        Returns:
            UserDTO - Data Transfer Object representing user profile.
        """

        return UserDTO(
            id=user.pk,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar=user.avatar.url if user.avatar else None,
            date_joined=user.date_joined,
        )
