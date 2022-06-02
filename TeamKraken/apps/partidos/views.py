from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from apps.utils.views import MultipleFieldLookupMixin

from .serializers import *
from .models import *

# Create your views here.

# -------------- PARTIDOS --------------

class ListaPartidos(ListAPIView):

    serializer_class = ListaPartidosSerializer

    def get_queryset(self):
        
        username = self.kwargs['username']
        equipo_id = self.kwargs['equipo_id']

        if username and equipo_id:
            queryset = Partido.objects.filter(equipo__id=equipo_id, equipo__user__username=username)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )


class DetallesPartido(MultipleFieldLookupMixin, RetrieveAPIView):

    queryset = Partido.objects.all()
    serializer_class = DetallesPartidoSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


# Crea un partido y los informes de partidos a los convocados (únicamente con los datos del partido y del jugador)
class CrearPartido(CreateAPIView):

    serializer_class = NuevoPartidoSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = NuevoPartidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuevoPartido = Partido.objects.create(
            fecha = serializer.validated_data['fecha'],
            temporada = serializer.validated_data['temporada'],
            local = serializer.validated_data['local'],
            visitante = serializer.validated_data['visitante'],
            goles_local = serializer.validated_data['goles_local'],
            goles_visitante = serializer.validated_data['goles_visitante'],
            equipo = serializer.validated_data['equipo'],
        )

        jugadores_convocados = serializer.validated_data['convocados']

        informes_jugadores = []

        for jugador in jugadores_convocados:

            informe_jugador = DatosPartido(
                partido = nuevoPartido,
                jugador = jugador
            )

            informes_jugadores.append(informe_jugador)

        DatosPartido.objects.bulk_create(informes_jugadores)

        return Response({'created' : nuevoPartido.id})


class ActualizarPartido(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Partido.objects.all()
    serializer_class = ListaPartidosSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']

    
class EliminarPartido(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Partido.objects.all()
    serializer_class = ListaPartidosSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


# -------------- INFORMES --------------

class DetallesInformePartido(MultipleFieldLookupMixin, RetrieveAPIView):
    
    queryset = DatosPartido.objects.all()
    serializer_class = DetallesInformesSerializer

    lookup_fields = ['partido__equipo__user__username','partido__equipo__id','id']


class CrearInformePartido(CreateAPIView):

    serializer_class = CrearActualizarEliminarDetallesInformesSerializer
    

class ActualizarInformePartido(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = DatosPartido.objects.all()
    serializer_class = CrearActualizarEliminarDetallesInformesSerializer

    lookup_fields = ['partido__equipo__user__username','partido__equipo__id','id']

    
class EliminarInformePartido(MultipleFieldLookupMixin, DestroyAPIView):
    
    queryset = DatosPartido.objects.all()
    serializer_class = CrearActualizarEliminarDetallesInformesSerializer

    lookup_fields = ['partido__equipo__user__username','partido__equipo__id','id']