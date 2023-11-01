from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("registration/", views.registration),
    path("login/", views.log_in),
    path("logout/", views.log_out),
    path("profile/", views.get_profile),
    path("profile/update", views.update_profile, name="update_profile"),
]
