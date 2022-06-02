from django.urls import path

from .views import *


urlpatterns = [

    # -------------- PARTIDOS --------------

    # Lista de partidos por equipo y usuario
    path('list/<username>/<equipo_id>/', ListaPartidos.as_view()),
    # Detalles de un partido
    path('detail/<equipo__user__username>/<equipo__id>/<id>/', DetallesPartido.as_view()),
    # # Crear partido
    path('create/<username>/', CrearPartido.as_view()),
    # # Actualizar un partido
    path('update/<equipo__user__username>/<equipo__id>/<id>/', ActualizarPartido.as_view()),
    # # Eliminar un partido
    path('delete/<equipo__user__username>/<equipo__id>/<id>/', EliminarPartido.as_view()),

    # -------------- INFORMES --------------
    
    # Detalles de un informe de partido
    path('detail/<partido__equipo__user__username>/<partido__equipo__id>/informe/<id>/', DetallesInformePartido.as_view()),
    # Crear un informe de partido
    path('create/<username>/informe/', CrearInformePartido.as_view()),
    # Actualizar un informe de partido
    path('update/<partido__equipo__user__username>/<partido__equipo__id>/informe/<id>/', ActualizarInformePartido.as_view()),
    # Eliminar un informe de partido
    path('delete/<partido__equipo__user__username>/<partido__equipo__id>/informe/<id>/', EliminarInformePartido.as_view()),
]
