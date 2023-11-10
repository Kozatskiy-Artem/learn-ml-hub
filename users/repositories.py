from annoying.functions import get_object_or_None

from core.exceptions import InstanceNotExistError

from .dto import UpdateUserDTO, UserDTO
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

        user = self._get_user_by_id(user_id=user_id)
        return self._user_to_dto(user)

    def update_profile(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        """
        Update user profile based on the provided data.

        Args:
            update_user_dto (UpdateUserDTO): Data transfer object containing updated user information.

        Returns:
            UserDTO - Data transfer object representing the updated user profile.

        Raises:
            InstanceNotExistError: If the user with the provided ID does not exist.
        """

        user = self._get_user_by_id(user_id=update_user_dto.id)

        user.first_name = update_user_dto.first_name
        user.last_name = update_user_dto.last_name
        if update_user_dto.avatar:
            user.avatar = update_user_dto.avatar
        user.save()

        return self._user_to_dto(user)

    def delete_profile(self, user_id: int) -> None:
        user = self._get_user_by_id(user_id=user_id)

        user.delete()

    @staticmethod
    def _get_user_by_id(user_id: int) -> UserModel:
        """
        Retrieve user model object by user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            UserModel - User model object.

        Raises:
            InstanceNotExistError: If the user with the given ID does not exist or is not active.
        """

        user = get_object_or_None(UserModel, id=user_id)
        if not user or not user.is_active:
            raise InstanceNotExistError(message=f"User with given id={user_id} does not exist error")

        return user

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
