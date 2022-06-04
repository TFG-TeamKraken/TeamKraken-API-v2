from django.urls import path

from .views import *

urlpatterns = [

    # Lista de ejercicios por usuario
    path('list/<username>/', ListaEjerciciosFiltrada.as_view()),
    # Detalles de un ejercicio
    path('detail/<user__username>/<id>/', DetallesEjercicio.as_view()),
    # Búsqueda de nuevos ejercicios
    path('fetch/<user__username>/', FetchEjercicios.as_view()),
    # Crear ejercicio
    path('create/<username>/', CrearEjercicio.as_view()),
    # Actualizar un ejercicio
    path('update/<user__username>/<id>/', ActualizarEjercicio.as_view()),
    # Eliminar un ejercicio
    path('delete/<user__username>/<id>/', EliminarEjercicio.as_view()),
]