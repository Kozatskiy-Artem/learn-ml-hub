from django.db import models

from users.models import UserModel


class ImageModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")


class ClassificationModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="models")
    filters_1_layer = models.PositiveIntegerField()
    filters_2_layer = models.PositiveIntegerField()
    filters_3_layer = models.PositiveIntegerField()
    dense_neurons = models.PositiveIntegerField()
    epochs = models.PositiveIntegerField()
    weights_path = models.CharField(max_length=50)


class HistoryModel(models.Model):
    model = models.ForeignKey(to=ClassificationModel, on_delete=models.CASCADE, related_name="history")
    epoch_number = models.PositiveIntegerField()
    accuracy = models.FloatField()
    val_accuracy = models.FloatField()
    loss = models.FloatField()
    val_loss = models.FloatField()
