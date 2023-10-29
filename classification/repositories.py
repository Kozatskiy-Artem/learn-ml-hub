from .interfaces import ImageRepositoryInterface
from .models import ImageModel


class ImageRepository(ImageRepositoryInterface):
    """
    A repository for managing image data in the application.

    This class implements the ImageRepositoryInterface and provides methods
    for saving image information to the database.

    Methods:

    - save_image(user, title, image_path): Saves image information to the database.
    """

    def save_image(self, user, title: str, image_path: str) -> ImageModel:
        """
        Saves image information to the database.

        Args:
            user: The user model object who uploaded the image.
            title (str): The title of the image.
            image_path (str): The file path of the image.

        Returns:
            ImageModel - The created ImageModel object.

        """

        image = ImageModel.objects.create(user=user, title=title, image=image_path)

        return image
