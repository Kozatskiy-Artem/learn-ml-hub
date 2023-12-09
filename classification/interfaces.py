from abc import ABCMeta, abstractmethod

from .dto import CreateImageDTO


class ImageRepositoryInterface(metaclass=ABCMeta):
    """
    An interface for managing image data in the application.

    This abstract class defines the methods that should be implemented by
    concrete classes acting as repositories for saving image information.

    Methods:

    - save_image(user, title, image_path): Abstract method to save image information.
    """

    @abstractmethod
    def save_image(self, image_dto: CreateImageDTO):
        """
        Abstract method to save image information to the repository.

        Args:
            image_dto: The user model object who uploaded the image.
        """
        pass
