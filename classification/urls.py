from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("", views.cats_or_dogs, name="cats_or_dogs"),
]
