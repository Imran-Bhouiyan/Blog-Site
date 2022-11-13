from django import views
from django.urls import path
from . views import *
from . import views
urlpatterns = [
    path("register/" , views.register ),
    path("login_otp_send/" , views.login_otp_send),
    path("login/" , views.login),

]