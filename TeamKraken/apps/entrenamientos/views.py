from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from apps.utils.views import MultipleFieldLookupMixin

from .serializers import *
from .models import *


# Create your views here.

# -------------- Entrenamientos --------------

class ListaEntrenamientos(ListAPIView):

    serializer_class = ListaEntrenamientosSerializer

    def get_queryset(self):
        
        username = self.kwargs['username']
        equipo_id = self.kwargs['equipo_id']

        if username and equipo_id:
            queryset = Entrenamiento.objects.filter(equipo__id=equipo_id, equipo__user__username=username)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )


class DetallesEntrenamiento(MultipleFieldLookupMixin, RetrieveAPIView):

    queryset = Entrenamiento.objects.all()
    serializer_class = DetallesEntrenamientoSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


class CrearEntrenamiento(CreateAPIView):

    serializer_class = NuevoEntrenamientoSerializer

    def create(self, request, *args, **kwargs):

        serializer = NuevoEntrenamientoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuevoEntrenamiento = Entrenamiento.objects.create(
            fecha = serializer.validated_data['fecha'],
            tipo_entrenamiento = serializer.validated_data['tipo_entrenamiento'],
            equipo = serializer.validated_data['equipo']
        )

        nuevoEntrenamiento.ejercicios.set(serializer.validated_data['ejercicios'])
        nuevoEntrenamiento.jugadores.set(serializer.validated_data['jugadores'])
        equipo_asociado = serializer.validated_data['equipo']

        # ------- Creación de faltas de asistencia -------

        # Obtenemos el id del equipo y obtenemos la lista de jugadores del mismo
        jugadores_equipo_all = Jugador.objects.filter(equipo = equipo_asociado)

        jugadores_equipo_all_objects = []

        for jugador_id in jugadores_equipo_all:
            jugadores_equipo_all_objects.append(jugador_id)

        jugadores_asistentes = []
            
        for jugador in serializer.validated_data['jugadores']:
            jugadores_asistentes.append(jugador)

        # Obtenemos la lista de jugadores que han asistido al entrenamiento y extraemos la diferencia entre 
        # esta y la lista de todos los jugadores, obteniendo los jugadores que no han asistido.
        jugadores_no_asistidos = list(set(jugadores_equipo_all_objects) - set(jugadores_asistentes))

        # Creamos las faltas de asistencia para cada jugador obtenido
        faltas_jugadores = []

        for jugador in jugadores_no_asistidos:

            falta_jugador = FaltaAsistencia(
                entrenamiento = nuevoEntrenamiento,
                jugador = jugador
            )

            faltas_jugadores.append(falta_jugador)

        # ------- Creación de informes de entrenamientos -------

        informes_entrenamientos = []

        for jugador in jugadores_asistentes:

            informe_jugador = DatosEntrenamiento(
                entrenamiento = nuevoEntrenamiento,
                jugador = jugador
            )

            informes_entrenamientos.append(informe_jugador)

        DatosEntrenamiento.objects.bulk_create(informes_entrenamientos)
        FaltaAsistencia.objects.bulk_create(faltas_jugadores)

        return Response({'created' : nuevoEntrenamiento.id})


class ActualizarEntrenamiento(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Entrenamiento.objects.all()
    serializer_class = EditEntrenamientoSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']


class EliminarEntrenamiento(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Entrenamiento.objects.all()
    serializer_class = EditEntrenamientoSerializer

    lookup_fields = ['equipo__user__username','equipo__id','id']

# -------------- INFORMES --------------

class DetallesInformeEntrenamiento(MultipleFieldLookupMixin, RetrieveAPIView):

    queryset = DatosEntrenamiento.objects.all()
    serializer_class = InformeSerializer

    lookup_fields = ['entrenamiento__equipo__user__username','entrenamiento__equipo__id','id']


class CrearInformeEntrenamiento(CreateAPIView):

    serializer_class = CrearActualizarEliminarDetallesInformesSerializer


class ActualizarInformeEntrenamiento(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = DatosEntrenamiento.objects.all()
    serializer_class = CrearActualizarEliminarDetallesInformesSerializer

    lookup_fields = ['entrenamiento__equipo__user__username','entrenamiento__equipo__id','id']

    
class EliminarInformeEntrenamiento(MultipleFieldLookupMixin, DestroyAPIView):
    
    queryset = DatosEntrenamiento.objects.all()
    serializer_class = CrearActualizarEliminarDetallesInformesSerializer

    lookup_fields = ['entrenamiento__equipo__user__username','entrenamiento__equipo__id','id']