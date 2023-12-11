from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("cats_or_dogs", views.cats_or_dogs, name="cats_or_dogs"),
    path("cats_or_dogs_pre_trained", views.cats_or_dogs_pre_trained_model, name="cats_or_dogs_pre_trained_model"),
    path("create_model", views.create_model, name="create_model"),
    path("user_model/<int:model_id>", views.get_user_model, name="user_model"),
    path("user_models", views.get_user_models, name="user_models"),
]
