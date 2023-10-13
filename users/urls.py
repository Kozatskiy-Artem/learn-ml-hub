from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration),
    path('login/', views.log_in),
    path("logout/", views.log_out),
]
