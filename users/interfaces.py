from abc import ABCMeta, abstractmethod


class UserRepositoryInterface(metaclass=ABCMeta):
    """
    An interface for managing user profile data in the application.

    This abstract class defines the methods that should be implemented by
    concrete classes acting as repositories for saving user profile information.

    Methods:

    - get_profile(user_id): Abstract method to get user profile information.
    """

    @abstractmethod
    def get_profile(self, user_id):
        pass

    @abstractmethod
    def update_profile(self, update_user_dto):
        pass
