"""TeamKraken URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluimos el resto de URLS
    # Auth
    re_path('api/auth/', include('apps.authentication.urls')),
    # Equipos
    re_path('api/equipos/', include('apps.equipos.urls')),
    # Jugadores
    re_path('api/jugadores/', include('apps.jugadores.urls')),
    # Partidos
    re_path('api/partidos/', include('apps.partidos.urls')),
    # Ejercicios
    re_path('api/ejercicios/', include('apps.ejercicios.urls'))
]
