from django.urls import path
from . import views


app_name = 'info_pages'

urlpatterns = [
    path('', views.home, name='home'),
]
