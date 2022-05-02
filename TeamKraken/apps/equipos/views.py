from django.shortcuts import render
from rest_framework.generics import *

from apps.utils.views import MultipleFieldLookupMixin

from .models import Equipo
from .serializers import *

import json
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# -------------- EQUIPOS --------------

# Lista de todos los equipos -- INÚTIL
class ListaEquipos(ListAPIView):

    serializer_class = ListaEquiposSerializer

    def get_queryset(self):
        return Equipo.objects.all()


# Lista de equipos por usuario
class ListaEquiposPorUsuario(ListAPIView):

    serializer_class = ListaEquiposSerializer

    def get_queryset(self):
        
        queryset = Equipo.objects.all()
        username = self.kwargs['username']

        if username is not None:
            queryset = queryset.filter(user__username=username)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )


class DetallesEquipo(MultipleFieldLookupMixin, RetrieveAPIView):

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    lookup_fields = ['user__username', 'id']


class CrearEquipo(CreateAPIView):

    serializer_class = EquipoSerializer


class ActualizarEquipo(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    lookup_fields = ['user__username', 'id']


class EliminarEquipo(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    lookup_fields = ['user__username', 'id']


# -------------- NOTAS --------------

class ListaNotasPorEquipo(ListAPIView):
    
    serializer_class = ListaNotasSerializer

    def get_queryset(self):
        
        queryset = Nota.objects.all()
        username = self.kwargs['username']
        equipoId = self.kwargs['equipoId']

        if username is not None and equipoId is not None:
            queryset = queryset.filter(equipo__user__username=username, equipo__id=equipoId)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )


class DetallesNota(MultipleFieldLookupMixin, RetrieveAPIView):

    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

    lookup_fields = ['equipo__user__username', 'equipo__id', 'id']


class CrearNota(CreateAPIView):

    serializer_class = NotaSerializer


class ActualizarNota(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

    lookup_fields = ['equipo__user__username', 'equipo__id', 'id']


class EliminarNota(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

    lookup_fields = ['equipo__user__username', 'equipo__id', 'id']