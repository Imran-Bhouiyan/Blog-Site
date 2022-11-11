from django import views
from django.urls import path
from . views import *
from . import views
urlpatterns = [
    path("register/" , views.register ),
]