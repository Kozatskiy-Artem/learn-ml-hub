from django.urls import path

from . import views

app_name = "info_pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("ml/", views.ml_page, name="ml"),
    path("ml/types/", views.ml_types_page, name="ml_types"),
    path("neural_networks/", views.neural_networks_page, name="neural_networks"),
    path("deep_learning/", views.deep_learning_page, name="deep_learning"),
]
