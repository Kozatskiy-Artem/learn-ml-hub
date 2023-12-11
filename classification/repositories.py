from annoying.functions import get_object_or_None

from users.models import UserModel

from .dto import CreateImageDTO, HistoryDTO, ImageDTO, ModelDTO
from .interfaces import ImageRepositoryInterface
from .models import ClassificationModel, HistoryModel, ImageModel


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


class ClassificationModelRepository:
    """
    Repository for managing Classification Models.

    This repository provides methods to create, retrieve, and manipulate Classification Models
    and their associated training history.

    Methods:

    - create_model: Create a new Classification Model with specified hyperparameters, weights, and training history.
    """

    def create_model(self, user, hyper_params_dto, weights_path, history) -> ModelDTO:
        """
        Create a new Classification Model with the provided parameters.

        Args:
            user: The user associated with the model.
            hyper_params_dto: Data transfer object containing hyperparameters for model creation.
            weights_path: The path to the pre-trained weights for the model.
            history: The training history of the model.

        Returns:
            ModelDTO - Data transfer object containing information about the created model.
        """

        model = ClassificationModel.objects.create(
            user=user,
            filters_1_layer=hyper_params_dto.filters_1_layer,
            filters_2_layer=hyper_params_dto.filters_2_layer,
            filters_3_layer=hyper_params_dto.filters_3_layer,
            dense_neurons=hyper_params_dto.dense_neurons,
            epochs=hyper_params_dto.epochs,
            weights_path=weights_path,
        )

        accuracy = history.history["accuracy"]
        val_accuracy = history.history["val_accuracy"]
        loss = history.history["loss"]
        val_loss = history.history["val_loss"]

        model_history = []
        for index in range(len(accuracy)):
            model_history.append(
                HistoryModel.objects.create(
                    model=model,
                    epoch_number=index + 1,
                    val_accuracy=val_accuracy[index],
                    accuracy=accuracy[index],
                    loss=loss[index],
                    val_loss=val_loss[index],
                )
            )
        history_list_dto = self._history_to_list_dto(model_history)
        return self._model_to_dto(model, history_list_dto)

    @staticmethod
    def _model_to_dto(model: ClassificationModel, history_list_dto) -> ModelDTO:
        """
        Convert a ClassificationModel instance to a ModelDTO.

        Args:
            model (ClassificationModel): The model instance.

        Returns:
            ModelDTO - Data Transfer Object representing model data.
        """

        return ModelDTO(
            id=model.pk,
            user_id=model.user.pk,
            filters_1_layer=model.filters_1_layer,
            filters_2_layer=model.filters_2_layer,
            filters_3_layer=model.filters_3_layer,
            dense_neurons=model.dense_neurons,
            epochs=model.epochs,
            weights_path=model.weights_path,
            history=history_list_dto,
        )

    @staticmethod
    def _history_to_dto(history: HistoryModel) -> HistoryDTO:
        """
        Convert a HistoryModel instance to a HistoryDTO.

        Args:
            history (HistoryModel): The history instance.

        Returns:
            HistoryDTO - Data Transfer Object representing history data.
        """
        return HistoryDTO(
            id=history.pk,
            class_model_id=history.model.pk,
            epoch_number=history.epoch_number,
            accuracy=history.accuracy,
            val_accuracy=history.val_accuracy,
            loss=history.loss,
            val_loss=history.val_loss,
        )

    def _history_to_list_dto(self, history: list[HistoryModel]) -> list[HistoryDTO]:
        """
        Converts a list of HistoryModel objects to a list of HistoryDTO objects.

        Args:
            history (list[HistoryModel]): A list of HistoryModel objects to be converted.

        Returns:
            list[HistoryDTO] - A list of HistoryDTO objects containing the converted data.
        """
        history_list_dto = [self._history_to_dto(epoch) for epoch in history]

        return history_list_dto
