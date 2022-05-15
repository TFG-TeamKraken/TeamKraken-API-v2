from rest_framework import serializers
from apps.jugadores.models import Posicion
from apps.jugadores.models import Jugador

from apps.authentication.serializers import UserSerializer

from .models import *

class ListaEquiposSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipo
        fields = (
            'id',
            'nombre',
            'categoria',
            'temporada'
        )


class EquipoSerializer(serializers.ModelSerializer):

    notas = serializers.SerializerMethodField()
    jugadores = serializers.SerializerMethodField()

    class Meta:
        model = Equipo
        fields = (
            'id',
            'id_equipo',
            'nombre',
            'nombre_club',
            'temporada',
            'categoria',
            'domicilio',
            'localidad',
            'provincia',
            'codigo_postal',
            'cod_club',
            'cod_equipo',
            'cod_temporada',
            'cod_grupo',
            'cod_competicion',
            'creado_manual',
            'user',
            'jugadores',
            'notas'
        )

    def get_notas(self, obj):
        query = Nota.objects.filter(equipo__id=obj.id)
        notas_serializadas = ListaNotasSerializer(query, many=True).data
        return notas_serializadas
        
    def get_jugadores(self, obj):
        query = Jugador.objects.filter(equipo__id=obj.id)
        jugadores_serializados = ListaJugadoresSerializer(query, many=True).data
        return jugadores_serializados


class PosicionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posicion
        fields = (
            'abreviacion',
        )

class ListaJugadoresSerializer(serializers.ModelSerializer):

    posicion_principal = PosicionSerializer()

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos',
            'posicion_principal'
        )

class ListaNotasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nota
        fields = (
            'id',
            'fecha_creacion',
            'texto'
        )

class NotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nota
        fields = (
            'id',
            'fecha_creacion',
            'texto',
            'equipo'
        )