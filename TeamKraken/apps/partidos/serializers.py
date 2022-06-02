from rest_framework import serializers

from .models import *

class ListaPartidosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partido
        fields = (
            'id',
            'fecha',
            'temporada',
            'local',
            'visitante',
            'goles_local',
            'goles_visitante'
        )


class PosicionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posicion
        fields = (
            'id',
            'abreviacion',
        )

class ListaConvocadosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos'
        )

class ListaInformesSerializer(serializers.ModelSerializer):

    jugador = ListaConvocadosSerializer()
    posicion_jugada = PosicionSerializer()

    class Meta:
        model = DatosPartido
        fields = (
            'id',
            'goles',
            'asistencias',
            'valoracion_partido',
            'posicion_jugada',
            'jugador'
        )


class DetallesPartidoSerializer(serializers.ModelSerializer):

    # convocados = ListaConvocadosSerializer(many=True)
    informes = serializers.SerializerMethodField()

    class Meta:
        model = Partido
        fields = (
            'id',
            'fecha',
            'temporada',
            'local',
            'visitante',
            'goles_local',
            'goles_visitante',
            'convocados',
            'informes'
        )

    def get_informes(self, obj):
        query = DatosPartido.objects.filter(partido__id=obj.id)
        informes_serializados = ListaInformesSerializer(query, many=True).data
        return informes_serializados


class NuevoPartidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partido
        fields = (
            'id',
            'fecha',
            'temporada',
            'local',
            'visitante',
            'goles_local',
            'goles_visitante',
            'convocados',
            'equipo'
        )


class DetallesInformesSerializer(serializers.ModelSerializer):

    partido = ListaPartidosSerializer()
    jugador = ListaConvocadosSerializer()
    posicion_jugada = PosicionSerializer()

    class Meta:
        model = DatosPartido
        fields = (
            'id',
            'titular',
            'valoracion_partido',
            'posicion_jugada',
            'tiros_puerta',
            'goles',
            'asistencias',
            'paradas',
            'goles_encajados',
            'robos_balon',
            'balones_perdidos',
            'pases_cortados',
            'minutos_jugados',
            'plus_minutos_por_lesion',
            'amarillas',
            'rojas',
            'jugador',
            'partido'
        )


class CrearActualizarEliminarDetallesInformesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatosPartido
        fields = (
            'id',
            'titular',
            'valoracion_partido',
            'posicion_jugada',
            'tiros_puerta',
            'goles',
            'asistencias',
            'paradas',
            'goles_encajados',
            'robos_balon',
            'balones_perdidos',
            'pases_cortados',
            'minutos_jugados',
            'plus_minutos_por_lesion',
            'amarillas',
            'rojas',
            'jugador',
            'partido'
        )