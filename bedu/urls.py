"""bedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from rest_framework import routers

from travels import views

router = routers.DefaultRouter()
router.register(r'/users', views.UserViewSet)
router.register(r'/zonas', views.ZonaViewSet)
router.register(r'/tours', views.TourViewSet)
router.register(r'/salidas', views.SalidaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travels.urls')),
    path('api/buy-ticket/', views.BuyTicket.as_view()),
    path('api', include(router.urls)),
    path('api/auth', include("rest_framework.urls", namespace="rest_framework")),
    path('graphql', GraphQLView.as_view(graphiql=True)),
]


# curl -X POST -H "Content-Type:application/json" -d '{"nombre":"Carlos","apellidos":"Perez","email":"charly@mail","fechaNacimiento":"1990-02-03","genero":"H","clave":null,"tipo":null}' http://localhost:8000/api/users/