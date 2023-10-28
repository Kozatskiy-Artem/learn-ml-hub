from abc import ABCMeta, abstractmethod


class ImageRepositoryInterface(metaclass=ABCMeta):
    """
    An interface for managing image data in the application.

    This abstract class defines the methods that should be implemented by
    concrete classes acting as repositories for saving image information.

    Methods:

    - save_image(user, title, image_path): Abstract method to save image information.
    """

    @abstractmethod
    def save_image(self, user, title: str, image_path: str):
        """
        Abstract method to save image information to the repository.

        Args:
            user: The user model object who uploaded the image.
            title (str): The title of the image.
            image_path (str): The file path of the image.
        """
        pass
