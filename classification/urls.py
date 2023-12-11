from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("cats_or_dogs", views.cats_or_dogs, name="cats_or_dogs"),
    path("cats_or_dogs_pre_trained", views.cats_or_dogs_pre_trained_model, name="cats_or_dogs_pre_trained_model"),
    path("create_model", views.create_model, name="create_model"),
]
