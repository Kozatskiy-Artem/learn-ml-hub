import keras
from PIL import Image
import numpy as np

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

    def get_prediction(self, user, title: str, image):
        """
        Get a prediction for the provided image.

        Args:
           user: The user model object who uploaded the image.
           title (str): The title of the image.
           image: The image file.

        Returns:
           (image_instance, result) - A tuple containing the saved image instance and the classification result.
        """

        img = self._resize_image(image)

        image_instance = self._save_image(user=user, title=title, image=img, image_name=image.name)

        img_array = self._normalize_image(img)

        model = self.get_model()

        prediction = model.predict(img_array)

        if prediction[0] > 0.5:
            result = "Зображення містить собаку."
        else:
            result = "Зображення містить кішку."

        return image_instance, result

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

    def _save_image(self, user, title, image, image_name):
        """
        Save the image and its information.

        Args:
            user: The user model object who uploaded the image.
            title (str): The title of the image.
            image: The image file.
            image_name (str): The name of the image file.

        Returns:
            ImageModel: The saved image instance.

        """

        image_path = 'images/' + image_name
        image.save("media/" + image_path)

        image = self.image_repository.save_image(user=user, title=title, image_path=image_path)

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

    @staticmethod
    def get_model():
        """
        Get the pre-trained classification model.

        Returns:
            keras.Model - The pre-trained classification model.

        """

        model = keras.models.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Flatten(),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(loss='binary_crossentropy',
                      optimizer=keras.optimizers.RMSprop(learning_rate=1e-4),
                      metrics=['accuracy'])
        model.load_weights("./classification/weights.h5")

        return model
