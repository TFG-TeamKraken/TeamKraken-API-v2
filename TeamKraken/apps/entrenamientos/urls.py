from django.urls import path

from .views import *


urlpatterns = [

    # -------------- ENTRENAMIENTOS --------------

    # # Lista de entrenamientos por equipo y usuario
    # path('list/<username>/<equipo_id>/', ListaEntrenamientos.as_view()),
    # # Detalles de un entrenamiento
    # path('detail/<equipo__user__username>/<equipo__id>/<id>/', DetallesEntrenamiento.as_view()),
    # # # Crear entrenamiento
    # path('create/<username>/', CrearEntrenamiento.as_view()),
    # # # Actualizar un entrenamiento
    # path('update/<equipo__user__username>/<equipo__id>/<id>/', ActualizarEntrenamiento.as_view()),
    # # # Eliminar un entrenamiento
    # path('delete/<equipo__user__username>/<equipo__id>/<id>/', EliminarEntrenamiento.as_view()),

    # -------------- INFORMES --------------
    
    # # Detalles de un informe de partido
    # path('detail/<partido__equipo__user__username>/<partido__equipo__id>/informe/<id>/', DetallesInformeEntrenamiento.as_view()),
    # # Crear un informe de partido
    # path('create/<username>/informe/', CrearInformeEntrenamiento.as_view()),
    # # Actualizar un informe de partido
    # path('update/<entrenamiento__equipo__user__username>/<entrenamiento__equipo__id>/informe/<id>/', ActualizarInformeEntrenamiento.as_view()),
    # # Eliminar un informe de partido
    # path('delete/<entrenamiento__equipo__user__username>/<entrenamiento__equipo__id>/informe/<id>/', EliminarInformeEntrenamiento.as_view()),
]