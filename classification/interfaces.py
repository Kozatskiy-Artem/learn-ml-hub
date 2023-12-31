from abc import ABCMeta, abstractmethod

from .dto import CreateImageDTO, ModelDTO, ModelListDTO


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


class ClassificationModelRepositoryInterface(metaclass=ABCMeta):
    """
    An interface for managing artificial neural network model data in the application.

    This abstract class defines methods that must be implemented by concrete classes
    that act as repositories for working with information of artificial neural network models.

    Methods:

    - create_model(self, user, hyper_params_dto, weights_path, history): Abstract method
      to save created model information.
    """

    @abstractmethod
    def create_model(self, user, hyper_params_dto, weights_path, history) -> ModelDTO:
        """
        Abstract method to save created model information to the repository.

        Args:
            user: The user associated with the model.
            hyper_params_dto: Data transfer object containing hyperparameters for model creation.
            weights_path: The path to the pre-trained weights for the model.
            history: The training history of the model.
        """
        pass

    @abstractmethod
    def get_user_model(self, user, model_id: int) -> ModelDTO:
        """
        Retrieve details of a specific classification model owned by the user.

        Args:
            user: The user associated with the model.
            model_id (int): The unique identifier of the model to retrieve.

        Returns:
            ModelDTO: Data transfer object containing information about the requested model.
        """
        pass

    @abstractmethod
    def get_user_models(self, user) -> list[ModelListDTO]:
        """
        Retrieve a list of classification models owned by the user.

        Args:
            user: The user associated with the models.

        Returns:
            list[ModelListDTO]: List of data transfer objects containing information about the user's models.
        """
        pass
