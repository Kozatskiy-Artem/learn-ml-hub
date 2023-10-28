from django.db import models

from users.models import UserModel


class ImageModel(models.Model):

    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")
