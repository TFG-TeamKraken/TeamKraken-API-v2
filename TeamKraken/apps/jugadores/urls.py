from django.urls import path

from .views import *

urlpatterns = [
    # Lista de jugadores por equipo
    path('list/<username>/<equipo_id>/', ListaJugadoresPorEquipoYUsuario.as_view()),
    # Detalles de un jugador
    path('detail/<equipo__user__username>/<equipo__id>/<id>/', DetallesJugador.as_view()),
    # Crear jugador
    path('create/<username>/', CrearJugador.as_view()),
    # Actualizar un jugador
    path('update/<equipo__user__username>/<equipo__id>/<id>/', ActualizarJugador.as_view()),
    # Eliminar un jugador
    path('delete/<equipo__user__username>/<equipo__id>/<id>/', EliminarJugador.as_view()),
    # Datos de todos los jugadores por posición
    path('datos_por_posicion/<username>/<equipo_id>/', DatosTodosJugadoresPorPosicion.as_view()),
]