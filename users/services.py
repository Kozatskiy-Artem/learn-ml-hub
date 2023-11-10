from PIL import Image

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

    def update_profile(self, update_user_dto):
        """
        Update user profile based on the provided data.

        Args:
            update_user_dto (UpdateUserDTO): Data transfer object containing updated user information.

        Returns:
            UserDTO - Data transfer object representing the updated user profile.

        Raises:
            InstanceNotExistError: If the user with the provided ID does not exist.
        """

        if update_user_dto.avatar:
            resized_avatar = self._resize_avatar(avatar=update_user_dto.avatar)
            avatar_url = self._save_avatar(avatar=resized_avatar, avatar_name=update_user_dto.avatar.name)

            update_user_dto.avatar = avatar_url

        return self.user_repository.update_profile(update_user_dto)

    def delete_profile(self, user_id: int) -> None:
        return self.user_repository.delete_profile(user_id=user_id)

    @staticmethod
    def _resize_avatar(avatar):
        """
        Resize the given avatar.

        Args:
            avatar: The avatar file.

        Returns:
            Image - The resized avatar.
        """

        resized_avatar = Image.open(avatar)
        resized_avatar = resized_avatar.resize((200, 200))

        return resized_avatar

    @staticmethod
    def _save_avatar(avatar, avatar_name):
        """
        Save the avatar.

        Args:
            avatar: The avatar file.
            avatar_name (str): The name of the avatar file.

        Returns:
            str: Avatar path.

        """

        avatar_path = "avatars/" + avatar_name
        avatar.save("media/" + avatar_path)

        return avatar_path
