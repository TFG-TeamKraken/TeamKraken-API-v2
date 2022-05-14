from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from apps.utils.views import MultipleFieldLookupMixin

from .serializers import *
from .models import *

# Create your views here.


# Lista de equipos por usuario
class ListaJugadoresPorEquipoYUsuario(ListAPIView):

    serializer_class = ListaJugadoresSerializer

    def get_queryset(self):
        
        username = self.kwargs['username']
        equipo_id = self.kwargs['equipo_id']

        if username and equipo_id:
            queryset = Jugador.objects.filter(equipo__id=equipo_id, equipo__user__username=username)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )


class DetallesJugador(MultipleFieldLookupMixin, RetrieveAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorConEstadisticasSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


class CrearJugador(CreateAPIView):

    serializer_class = JugadorSerializer


class ActualizarJugador(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


class EliminarJugador(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


class DatosTodosJugadoresPorPosicion(ListAPIView):

    serializer_class = DatosPosicion

    def get_queryset(self):
        
        username = self.kwargs['username']
        equipo_id = self.kwargs['equipo_id']

        if username and equipo_id:
            queryset = DatosPartido.objects.datos_por_posicion(username, equipo_id)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )
