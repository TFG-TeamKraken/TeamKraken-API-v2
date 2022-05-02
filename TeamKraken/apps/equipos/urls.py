from django import views
from django.urls import path

from .views import *


urlpatterns = [

    # -------------- EQUIPOS --------------

    # Lista de equipos por usuario
    path('list/<username>/', ListaEquiposPorUsuario.as_view()),
    # Detalles de un equipo
    path('detail/<user__username>/<id>/', DetallesEquipo.as_view()),
    # Crear equipo
    path('create/<username>/', CrearEquipo.as_view()),
    # Actualizar un equipo
    path('update/<user__username>/<id>/', ActualizarEquipo.as_view()),
    # Eliminar un equipo
    path('delete/<user__username>/<id>/', EliminarEquipo.as_view()),

    # -------------- NOTAS --------------

    # Lista de notas por equipo y usuario
    path('list/<username>/<equipoId>/notas/', ListaNotasPorEquipo.as_view()),
    # Detalles de una nota
    path('detail/<equipo__user__username>/<equipo__id>/notas/<id>/', DetallesNota.as_view()),
    # Crear nota
    path('create/<username>/notas/', CrearNota.as_view()),
    # Actualizar una nota
    path('update/<equipo__user__username>/<equipo__id>/notas/<id>/', ActualizarNota.as_view()),
    # Eliminar una nota
    path('delete/<equipo__user__username>/<equipo__id>/notas/<id>/', EliminarNota.as_view()),


]
