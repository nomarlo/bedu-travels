from django.urls import path, include
from rest_framework import routers

from . import views

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name="index"),
    path("login/",
         auth_views.LoginView.as_view(
             template_name="registration/login.html"),
         name="login"
         ),
    path("logout/",
         auth_views.LogoutView.as_view(next_page="/login/"),
         name="logout"
         ),
]
