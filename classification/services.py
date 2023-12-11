import os
import random
import string
import zipfile

import keras
import numpy as np
from PIL import Image

from .dto import CreateImageDTO, HyperParamsDTO, ImageDTO
from .interfaces import ClassificationModelRepositoryInterface, ImageRepositoryInterface


class ClassificationService:
    """
    A service class for image classification.

    This class provides methods for classifying images and building new artificial neural network models.

    Attributes:
        image_repository (ImageRepositoryInterface): An instance of the image repository.
        classification_model_repository (ClassificationModelRepositoryInterface):
          An instance of the classification model repository.

    Methods:

    - get_prediction(image_dto, model_name): Get a prediction for the provided image.
    - create_model(self, user, hyper_params_dto: HyperParamsDTO): Create a custom classification model based on
      the provided hyperparameters, train the model, save its weights,
      and store the model information in the repository.
    - get_user_model(self, user, model_id): Retrieve details of a specific classification model owned by the user.
    - get_user_models(self, user): Retrieve a list of classification models owned by the user.
    """

    def __init__(
        self,
        image_repository: ImageRepositoryInterface,
        classification_model_repository: ClassificationModelRepositoryInterface,
    ):
        self.image_repository = image_repository
        self.classification_model_repository = classification_model_repository

    def get_prediction(self, image_dto: CreateImageDTO, model_name: str, model_dto=None) -> tuple[ImageDTO, str]:
        """
        Get a prediction for an image using a classification model.

        Args:
            image_dto (CreateImageDTO): Data transfer object containing image information.
            model_name (str): Name of classification model
            model_dto: Data transfer object containing information about the requested model

        Returns:
            Tuple[ImageDTO, str] - A tuple containing the DTO of the saved image and the prediction result.
                - The first element is a CreateImageDTO object with information about the saved image.
                - The second element is a string indicating the prediction result,
                either "Image contains a dog." or "Image contains a cat."
        """

        resized_image = self._resize_image(image_dto.image)
        created_image_dto = self._save_image(image_dto, image=resized_image)
        image_array = self._normalize_image(resized_image)

        classification_model = self._get_model(model_name, model_dto)
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

    def _get_model(self, model_name: str, model_dto=None):
        """
        Retrieve a specific classification model based on the given model name.

        Args:
            model_name (str): The name of the model to retrieve. Valid options are:
                - "cats_or_dogs_model": Retrieve a model for classifying cats or dogs.
                - "cats_or_dogs_transfer_learned_model": Retrieve a transfer-learned model for classifying cats or dogs.
            model_dto: Data transfer object containing information about the model

        Returns:
            Any: The requested classification model. The specific type of the model depends on the provided model_name.
        """

        if model_name == "cats_or_dogs_model":
            return self._get_cats_or_dogs_model()
        elif model_name == "cats_or_dogs_transfer_learned_model":
            return self._get_cats_or_dogs_transfer_learned_model()
        elif model_name == "user_model":
            return self._get_custom_user_model(model_dto)

    @staticmethod
    def _get_cats_or_dogs_model():
        """
        Create and return a Sequential model for classifying cats or dogs.

        The model architecture consists of convolutional layers with max-pooling followed by fully connected layers.

        Returns:
            keras.models.Sequential: The created cats or dogs classification model.
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

        model.load_weights("./classification/weights.h5")

        return model

    @staticmethod
    def _get_cats_or_dogs_transfer_learned_model():
        """
        Create and return a transfer-learned InceptionV3-based model for classifying cats or dogs.

        The model uses the InceptionV3 architecture with additional dense layers for classification.

        Returns:
            keras.models.Model: The created transfer-learned cats or dogs classification model.
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

    def create_model(self, user, hyper_params_dto: HyperParamsDTO):
        """
        Create a custom classification model based on the provided hyperparameters, train the model,
        save its weights, and store the model information in the repository.

        Args:
            user: The user associated with the model.
            hyper_params_dto (HyperParamsDTO): Data transfer object containing hyperparameters for model creation.

        Returns:
            ModelDTO: Data transfer object containing information about the created model.
        """

        model = self._get_custom_user_model(hyper_params_dto)

        model.compile(
            loss="binary_crossentropy",
            optimizer=keras.optimizers.RMSprop(learning_rate=1e-4),
            metrics=["accuracy"],
        )

        train_generator, validation_generator = self._get_data()

        history = model.fit(
            train_generator,
            validation_data=validation_generator,
            steps_per_epoch=100,
            epochs=hyper_params_dto.epochs,
            validation_steps=50,
            verbose=2,
        )

        weights_path = "weights/custom_model_weights" + self._generate_random_string() + ".h5"
        model.save_weights(weights_path)

        return self.classification_model_repository.create_model(user, hyper_params_dto, weights_path, history)

    @staticmethod
    def _get_custom_user_model(hyper_params_dto: HyperParamsDTO):
        """
        Create and return a custom user-defined Sequential model based on the provided hyperparameters.

        Args:
            hyper_params_dto (HyperParamsDTO): Data transfer object containing hyperparameters for model creation.

        Returns:
            keras.models.Sequential: The created custom user-defined classification model.
        """

        model = keras.models.Sequential(
            [
                keras.layers.Conv2D(
                    hyper_params_dto.filters_1_layer, (3, 3), activation="relu", input_shape=(150, 150, 3)
                ),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Conv2D(
                    hyper_params_dto.filters_2_layer, (3, 3), activation="relu", input_shape=(150, 150, 3)
                ),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Conv2D(
                    hyper_params_dto.filters_3_layer, (3, 3), activation="relu", input_shape=(150, 150, 3)
                ),
                keras.layers.MaxPooling2D(2, 2),
                keras.layers.Flatten(),
                keras.layers.Dense(hyper_params_dto.dense_neurons, activation="relu"),
                keras.layers.Dense(1, activation="sigmoid"),
            ]
        )
        return model

    @staticmethod
    def _get_data():
        """
        Load and preprocess the training and validation data for model training.

        Returns:
            Tuple[keras.preprocessing.image.DirectoryIterator, keras.preprocessing.image.DirectoryIterator]:
                A tuple containing the training and validation data generators.
        """
        zip_ref = zipfile.ZipFile("cats_and_dogs_filtered.zip", "r")
        zip_ref.extractall("tmp/")
        zip_ref.close()

        base_dir = "tmp/cats_and_dogs_filtered"

        train_dir = os.path.join(base_dir, "train")
        validation_dir = os.path.join(base_dir, "validation")

        train_datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1.0 / 255.0,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
        )

        test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)

        train_generator = train_datagen.flow_from_directory(
            train_dir, batch_size=20, class_mode="binary", target_size=(150, 150)
        )

        validation_generator = test_datagen.flow_from_directory(
            validation_dir, batch_size=20, class_mode="binary", target_size=(150, 150)
        )

        return train_generator, validation_generator

    @staticmethod
    def _generate_random_string():
        """
        Generate a random string with a sequence of 10 characters.

        Returns:
            str: A string containing a random sequence of 10 characters.
        """

        random_chars = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        return random_chars

    def get_user_model(self, user, model_id):
        """
        Retrieve details of a specific classification model owned by the user.

        This method delegates the call to the associated classification model repository.

        Args:
            user: The user associated with the model.
            model_id: The unique identifier of the model to retrieve.

        Returns:
            ModelDTO: Data transfer object containing information about the requested model.
        """
        return self.classification_model_repository.get_user_model(user, model_id)

    def get_user_models(self, user):
        """
        Retrieve a list of classification models owned by the user.

        This method delegates the call to the associated classification model repository.

        Args:
            user: The user associated with the models.

        Returns:
            list[ModelListDTO]: List of data transfer objects containing information about the user's models.
        """
        return self.classification_model_repository.get_user_models(user)
