from annoying.functions import get_object_or_None

from users.models import UserModel

from .dto import CreateImageDTO, ImageDTO
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

    def save_image(self, image_dto: CreateImageDTO) -> ImageDTO:
        """
        Saves image information to the database.

        Args:
            image_dto: The user model object who uploaded the image.

        Returns:
            ImageDTO - The created ImageModel object.

        """

        user = get_object_or_None(UserModel, id=image_dto.user_id)

        image = ImageModel.objects.create(user=user, title=image_dto.title, image=image_dto.image)

        return self._user_to_dto(image)

    @staticmethod
    def _user_to_dto(image: ImageModel) -> ImageDTO:
        """
        Convert a ImageModel instance to a ImageDTO.

        Args:
            image (ImageModel): The image model instance.

        Returns:
            ImageDTO - Data Transfer Object representing image data.
        """

        return ImageDTO(id=image.pk, user_id=image.user.pk, title=image.title, image=image.image.url)
