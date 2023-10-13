from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class UserModel(AbstractUser):
    """Model for user object, inherited from AbstractUser"""

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="media/avatars/", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
