from .interfaces import UserRepositoryInterface


class UserService:
    """Service class for handling user-related operations."""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

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

        return self.user_repository.get_profile(user_id)
