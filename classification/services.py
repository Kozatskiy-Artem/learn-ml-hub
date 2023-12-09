import keras
import numpy as np
from PIL import Image

from .dto import CreateImageDTO, ImageDTO
from .interfaces import ImageRepositoryInterface


class ClassificationService:
    """
    A service class for image classification.

    This class provides methods for resizing, normalizing, saving and classifying images.

    Attributes:
        image_repository (ImageRepositoryInterface): An instance of the image repository.

    Methods:

    - get_prediction(user, title, image): Get a prediction for the provided image.

    """

    def __init__(self, image_repository: ImageRepositoryInterface):
        self.image_repository = image_repository

    def get_prediction(self, image_dto: CreateImageDTO, model_name: str):
        """
        Get a prediction for the provided image.

        Args:
           image_dto: The user model object who uploaded the image.

        Returns:
           (image_instance, result) - A tuple containing the saved image instance and the classification result.
        """

        resized_image = self._resize_image(image_dto.image)
        created_image_dto = self._save_image(image_dto, image=resized_image)
        image_array = self._normalize_image(resized_image)

        classification_model = self.get_model(model_name)
        prediction = classification_model.predict(image_array)

        if prediction[0] > 0.5:
            result = "Зображення містить собаку."
        else:
            result = "Зображення містить кота."

        return created_image_dto, result

    @staticmethod
    def _resize_image(image):
        """
        Resize the given image.

        Args:
            image: The image file.

        Returns:
            Image - The resized image.
        """

        resized_image = Image.open(image)
        resized_image = resized_image.resize((150, 150))

        return resized_image

    def _save_image(self, image_dto: CreateImageDTO, image: Image) -> ImageDTO:
        """
        Save the image and its information.

        Args:
            image_dto: The user model object who uploaded the image.
            image: The image file.

        Returns:
            ImageDTO: The saved image instance.

        """

        image_dto.image = "images/" + image_dto.image.name
        image.save("media/" + image_dto.image)

        image = self.image_repository.save_image(image_dto)

        return image

    @staticmethod
    def _normalize_image(image):
        """
        Normalize the given image.

        Args:
            image: The image file.

        Returns:
            numpy.ndarray - The normalized image array.

        """

        image_array = keras.preprocessing.image.img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0) / 255.0

        return image_array

    def get_model(self, model_name: str):
        if model_name == "cats_or_dogs_model":
            return self._get_cats_or_dogs_model()
        elif model_name == "cats_or_dogs_transfer_learned_model":
            return self._get_cats_or_dogs_transfer_learned_model()

    @staticmethod
    def _get_cats_or_dogs_model():
        """
        Get the pre-trained classification model.

        Returns:
            keras.Model - The pre-trained classification model.

        """

        model = keras.models.Sequential(
            [
                keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Conv2D(64, (3, 3), activation="relu"),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Conv2D(128, (3, 3), activation="relu"),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Conv2D(128, (3, 3), activation="relu"),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Flatten(),
                keras.layers.Dense(512, activation="relu"),
                keras.layers.Dense(1, activation="sigmoid"),
            ]
        )

        model.compile(
            loss="binary_crossentropy",
            optimizer=keras.optimizers.RMSprop(learning_rate=1e-4),
            metrics=["accuracy"],
        )
        model.load_weights("./classification/weights.h5")

        return model

    @staticmethod
    def _get_cats_or_dogs_transfer_learned_model():
        """
        Get the pre-trained classification model.

        Returns:
            keras.Model - The pre-trained classification model.

        """

        model = keras.applications.InceptionV3(input_shape=(150, 150, 3), include_top=False, weights=None)
        last_layer = model.get_layer("mixed7")
        last_output = last_layer.output
        x = keras.layers.Flatten()(last_output)
        x = keras.layers.Dense(1024, activation="relu")(x)
        x = keras.layers.Dense(512, activation="relu")(x)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.Dense(1, activation="sigmoid")(x)

        model = keras.Model(model.input, x)

        model.load_weights("./classification/transfer_learned_model_weights.h5")

        return model
